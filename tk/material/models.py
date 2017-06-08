import datetime

from django.db import models
from django.db.models import Subquery, Q
from django.utils.translation import ugettext as _

from localized_fields.fields import LocalizedField, LocalizedUniqueSlugField
from localized_fields.models import LocalizedModel

from .fields import LanguageField, LocalizedMarkdownxField


class Subject(models.Model):
    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    name = LocalizedField(max_length=512, verbose_name=_("name"))

    def __str__(self):
        return str(self.name)


class Goal(models.Model):
    class Meta:
        verbose_name = _("Goal")
        verbose_name_plural = _("Goals")

    name = LocalizedField(max_length=512, verbose_name=_("name"))

    def __str__(self):
        return str(self.name)


class GroupFeature(models.Model):
    class Meta:
        verbose_name = _("Group feature")
        verbose_name_plural = _("Group features")

    name = LocalizedField(max_length=512, verbose_name=_("name"))

    def __str__(self):
        return str(self.name)


class Location(models.Model):
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    name = LocalizedField(max_length=512, verbose_name=_("name"))

    def __str__(self):
        return str(self.name)


class Approval(models.Model):
    class Meta:
        verbose_name = _("Approval")
        verbose_name_plural = _("Approvals")

    material = models.OneToOneField('Material', on_delete=models.CASCADE)

    # TODO: Hide in forms
    requested = models.DateTimeField(auto_now_add=True, verbose_name=_("created on"))
    approved = models.BooleanField(default=False, verbose_name=_("is approved"))
    comment = models.TextField(blank=True, verbose_name=_("comment"))
    email = models.EmailField(blank=True, verbose_name=_("contact email"))

    def __str__(self):
        if self.approved:
            return _('Approved: "{}"').format(self.material)
        return _('Unapproved: "{}"').format(self.material)


class ApprovedQuerySet(models.QuerySet):
    def approved(self):
        bypassed = Q(approval__isnull=True)
        approved = Q(approval__approved=True)
        return self.filter(bypassed | approved)

    def unapproved(self):
        return self.filter(approval__approved=False)


class Material(LocalizedModel):
    objects = ApprovedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")

    title = LocalizedField(max_length=512, verbose_name=_("title"))
    slug = LocalizedUniqueSlugField(populate_from='title')

    # TODO: Required in all forms but activity forms
    subject = models.ForeignKey(Subject, null=True, on_delete=models.PROTECT,
            verbose_name=_("subject"))
    # TODO: Creation date
    brief = LocalizedMarkdownxField(blank=True, verbose_name=_("brief"))
    author = models.CharField(max_length=512, blank=True, verbose_name=_("author"))

    def __str__(self):
        return str(self.title)


class Activity(Material):
    objects = ApprovedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    goals = models.ManyToManyField(Goal, verbose_name=_("goals"))

    location = models.ForeignKey(Location, null=True, blank=True,
            on_delete=models.SET_NULL, verbose_name=_("location"))
    duration = models.DurationField(verbose_name=_("duration"))
    min_people = models.PositiveSmallIntegerField(default=2,
            verbose_name=_("minimum number of people"))
    max_people = models.PositiveSmallIntegerField(default=30,
            verbose_name=_("maximum number of people"))
    group_feature = models.ForeignKey(GroupFeature, null=True, blank=True,
            on_delete=models.SET_NULL, verbose_name=_("group feature"))
    notes = LocalizedField(blank=True, verbose_name=_("notes"))
    attachment = models.FileField(upload_to='material/activities/', blank=True,
            verbose_name=_("attachment"))
    url = models.URLField(blank=True, verbose_name=_("URL"),
            help_text=_("Link the material if its copyright does not allow sharing it."))

    def clean(self):
        if self.min_people > self.max_people:
            raise ValidationError(_("The upper bound for the people involved "
                "in the activity cannot be less than the lower bound."))


def validate_year(year):
    if datetime.date.today().year < year:
        raise ValidationError(_("That year is still in the future."))


class Reading(Material):
    objects = ApprovedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Reading")
        verbose_name_plural = _("Readings")

    pages = models.PositiveIntegerField(verbose_name=_("pages"))
    year = models.PositiveIntegerField(blank=True, null=True,
            validators=[validate_year], verbose_name=_("year"))
    languages = LanguageField(verbose_name=_("languages"))
    attachment = models.FileField(upload_to='material/readings/', blank=True,
            verbose_name=_("attachment"))
    url = models.URLField(blank=True, verbose_name=_("URL"),
            help_text=_("Link the material if its copyright does not allow sharing it."))


class Video(Material):
    objects = ApprovedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    duration = models.DurationField(verbose_name=_("duration"))
    year = models.PositiveIntegerField(validators=[validate_year], verbose_name=_("year"))
    audios = LanguageField(blank=True, verbose_name=_("audio languages"))
    subtitles = LanguageField(blank=True, verbose_name=_("subtitle languages"))
    attachment = models.FileField(upload_to='material/videos', blank=True,
            verbose_name=_("attachment"))
    url = models.URLField(blank=True, verbose_name=_("URL"),
            help_text=_("Link the material if its copyright does not allow sharing it."))


class Link(Material):
    objects = ApprovedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    url = models.URLField(verbose_name=_("URL"))
