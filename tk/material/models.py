import datetime
from psycopg2.extras import NumericRange

from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from django.db.models import Subquery, Q, F, Func
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.search import SearchVector, SearchRank
from django.contrib.postgres.fields import IntegerRangeField

from localized_fields.models import LocalizedModel
from localized_fields.fields import (
        LocalizedCharField, LocalizedTextField, LocalizedUniqueSlugField)

from .fields import LanguageField


COMMON_LANGUAGES = ['eu', 'es', 'fr', 'en']


class OnlyLocalizedName(models.Model):
    class Meta:
        abstract = True

    name = LocalizedCharField(
            max_length=512,
            required=False,
            verbose_name=_("name"))

    def __str__(self):
        return str(self.name)


class Subject(OnlyLocalizedName):
    class Meta:
        ordering = ['name']
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")


class GroupFeature(OnlyLocalizedName):
    class Meta:
        ordering = ['name']
        verbose_name = _("Group feature")
        verbose_name_plural = _("Group features")


class Location(OnlyLocalizedName):
    class Meta:
        ordering = ['name']
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")


class Approval(models.Model):
    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Approval")
        verbose_name_plural = _("Approvals")

    material = models.OneToOneField('Material', on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True,
            verbose_name=_("creation timestamp"))
    approved = models.BooleanField(default=False, verbose_name=_("is approved"))
    comment = models.TextField(blank=True, verbose_name=_("comment"))
    email = models.EmailField(blank=True, verbose_name=_("contact email"))

    def __str__(self):
        if self.approved:
            return _('Approved: "{}"').format(self.material)
        return _('Unapproved: "{}"').format(self.material)


class AVals(Func):
    function = 'avals'


class JoinArray(Func):
    function = 'array_to_string'
    template = "%(function)s(%(expressions)s, ' ')"


ConcatValues = lambda f : JoinArray(AVals(F(f)))


class MaterialQuerySet(models.QuerySet):
    SEARCH_VECTOR = SearchVector(ConcatValues('title'), weight='A')\
                  + SearchVector(ConcatValues('goal'), weight='B')\
                  + SearchVector(ConcatValues('brief'), weight='C')

    def search(self, query):
        return self\
            .approved()\
            .annotate(rank=SearchRank(MaterialQuerySet.SEARCH_VECTOR, query))\
            .order_by('-rank')\
            .filter(rank__gte=0.2)

    def approved(self):
        bypassed = Q(approval__isnull=True)
        approved = Q(approval__approved=True)
        return self.filter(bypassed | approved)

    def unapproved(self):
        return self.filter(approval__approved=False)


class Material(LocalizedModel):
    objects = MaterialQuerySet.as_manager()

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")

    title = LocalizedCharField(blank=False, null=False, required=False,
            max_length=512, verbose_name=_("title"))
    slug = LocalizedUniqueSlugField(populate_from='title')
    timestamp = models.DateTimeField(auto_now_add=True,
            verbose_name=_("creation timestamp"))

    subjects = models.ManyToManyField(Subject, verbose_name=_("subject"))
    goal = LocalizedTextField(blank=True, null=True, required=False,
            verbose_name=_("goal"))
    brief = LocalizedTextField(blank=False, null=False, required=False,
            verbose_name=_("brief"))
    author = models.CharField(max_length=512, blank=True, verbose_name=_("author"))

    def __str__(self):
        return str(self.title)

    def get_related(self):
        for related in ['activity', 'reading', 'video', 'link']:
            if hasattr(self, related):
                return getattr(self, related)

    def get_model_name(self):
        return self.get_related()._meta.model_name

    def get_absolute_url(self):
        return self.get_related().get_absolute_url()


class Activity(Material):
    objects = MaterialQuerySet.as_manager()

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    location = models.ForeignKey(Location, null=True, blank=True,
            on_delete=models.SET_NULL, verbose_name=_("location"))

    duration = models.PositiveSmallIntegerField(
            null=True,
            blank=True,
            verbose_name=_("duration"),
            help_text=_("Duration in minutes."),
    )

    num_people = IntegerRangeField(
            default=NumericRange(2, 30),
            verbose_name=_("number of people"))

    group_feature = models.ForeignKey(GroupFeature, null=True, blank=True,
            on_delete=models.SET_NULL, verbose_name=_("group feature"))
    notes = LocalizedTextField(null=True, blank=True, verbose_name=_("notes"))
    attachment = models.FileField(upload_to='material/activities/', blank=True,
            verbose_name=_("attachment"))
    url = models.URLField(blank=True, verbose_name=_("URL"),
            help_text=_("Link the material if its copyright does not allow sharing it."))

    def get_absolute_url(self):
        return reverse('material:detail-activity', kwargs={'slug': self.slug})

    def clean(self):
        if self.num_people.lower < 1:
            raise ValidationError(_("The lower bound must be at least 1."), code='invalid')


def validate_year(year):
    if datetime.date.today().year < year:
        raise ValidationError(_("That year is still in the future."),
                code='invalid')


class Reading(Material):
    objects = MaterialQuerySet.as_manager()

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Reading")
        verbose_name_plural = _("Readings")

    pages = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("pages"))
    year = models.PositiveIntegerField(blank=True, null=True,
            validators=[validate_year], verbose_name=_("year"))
    languages = LanguageField(limit_to=COMMON_LANGUAGES, verbose_name=_("languages"))
    url = models.URLField(blank=True, verbose_name=_("URL"),
            help_text=_("Link to the reading."))

    def get_absolute_url(self):
        return reverse('material:detail-reading', kwargs={'slug': self.slug})


class Video(Material):
    objects = MaterialQuerySet.as_manager()

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    duration = models.PositiveSmallIntegerField(
            verbose_name=_("duration"),
            help_text=_("Duration in minutes."),
    )

    year = models.PositiveIntegerField(null=True, blank=True,
            validators=[validate_year], verbose_name=_("year"))
    audios = LanguageField(blank=True, prioritize=COMMON_LANGUAGES,
            verbose_name=_("audio languages"))
    subtitles = LanguageField(blank=True, limit_to=COMMON_LANGUAGES,
            verbose_name=_("subtitle languages"))
    url = models.URLField(blank=True, verbose_name=_("URL"),
            help_text=_("Link to the video."))

    def get_absolute_url(self):
        return reverse('material:detail-video', kwargs={'slug': self.slug})


class Link(Material):
    objects = MaterialQuerySet.as_manager()

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    url = models.URLField(verbose_name=_("URL"))

    def get_absolute_url(self):
        return reverse('material:detail-link', kwargs={'slug': self.slug})
