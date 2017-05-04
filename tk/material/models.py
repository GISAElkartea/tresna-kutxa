import datetime

from django.db import models
from django.db.models import Subquery, Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.translation import ugettext as _

from autoslug import AutoSlugField


class Subject(models.Model):
    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    name = models.CharField(max_length=512, verbose_name=_("name"))

    def __str__(self):
        return self.name


class Goal(models.Model):
    class Meta:
        verbose_name = _("Goal")
        verbose_name_plural = _("Goals")

    name = models.CharField(max_length=512, verbose_name=_("name"))

    def __str__(self):
        return self.name


class GroupFeature(models.Model):
    class Meta:
        verbose_name = _("Group feature")
        verbose_name_plural = _("Group features")

    name = models.CharField(max_length=512, verbose_name=_("name"))

    def __str__(self):
        return self.name


class Location(models.Model):
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    name = models.CharField(max_length=512, verbose_name=_("name"))

    def __str__(self):
        return self.name


class Language(models.Model):
    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Language")

    name = models.CharField(max_length=512, verbose_name=_("name"))
    # TODO: Code?
    # TODO: Prepopulate
    # TODO: Autocomplete search interface

    def __str__(self):
        return self.name


class Approval(models.Model):
    class Meta:
        unique_together = [('content_type', 'object_id')]
        verbose_name = _("Approval")
        verbose_name_plural = _("Approvals")

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # TODO: Hide in forms
    requested = models.DateTimeField(auto_now_add=True, verbose_name=_("created on"))
    published = models.DateTimeField(null=True, blank=True, verbose_name=_("published on"))
    approved = models.BooleanField(default=False, verbose_name=_("is approved"))
    comment = models.TextField(null=True, verbose_name=_("comment"))
    email = models.EmailField(blank=True, verbose_name=_("contact email"))


A = Approval.objects.filter


class ApprovedQuerySet(models.QuerySet):
    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.model)

    def approved(self):
        acceptances = A(content_type=self.content_type, approved=True).values('object_id')
        approvals = A(content_type=self.content_type).values('object_id')
        qs = Q(id__in=Subquery(acceptances)) | ~Q(id__in=Subquery(approvals))
        return self.filter(qs)

    def unapproved(self):
        rejections = A(content_type=self.content_type, approved=False).values('object_id')
        return self.filter(id__in=Subquery(rejections))


class Material(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=512, verbose_name=_("title"))
    slug = AutoSlugField(populate_from='title', unique=True)

    subject = models.ForeignKey(Subject, verbose_name=_("subject"))
    brief = models.TextField(blank=True, verbose_name=_("brief"))
    author = models.CharField(max_length=512, blank=True, verbose_name=_("author"))
    # TODO: Add help text with the warning about copyright
    link = models.URLField(blank=True, verbose_name=_("link"))

    # TODO: Only display approved ones publicly
    # TODO: Display as link in admin
    approval = GenericRelation(Approval, verbose_name=_("Approval"))

    def __str__(self):
        return self.title


class Activity(Material):
    objects = ApprovedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    subject = models.ForeignKey(Subject, null=True, blank=True, verbose_name=_("subject"))
    goals = models.ManyToManyField(Goal, verbose_name=_("goals"))

    location = models.ForeignKey(Location, null=True, blank=True, verbose_name=_("location"))
    # TODO: Single point duration or range?
    duration = models.DurationField(verbose_name=_("duration"))
    # TODO: Single point num_people or range?
    num_people = models.PositiveSmallIntegerField(verbose_name=_("number of people"))
    group_feature = models.ForeignKey(GroupFeature, null=True, blank=True, verbose_name=_("group feature"))
    notes = models.TextField(blank=True, verbose_name=_("notes"))
    # TODO: Attachments generic relation


def validate_year(year):
    if datetime.date.today().year < year:
        raise ValidationError(_("That year is still in the future."))


class Reading(Material):
    objects = ApprovedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Reading")
        verbose_name_plural = _("Reading")

    pages = models.PositiveIntegerField(verbose_name=_("pages"))
    year = models.PositiveIntegerField(validators=[validate_year], verbose_name=_("year"))
    language = models.ForeignKey(Language, verbose_name=_("language"))
    # TODO: Attachments generic relation


class Video(Material):
    objects = ApprovedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    duration = models.DurationField(verbose_name=_("duration"))
    year = models.PositiveIntegerField(validators=[validate_year], verbose_name=_("year"))
    audios = models.ManyToManyField(Language, blank=True, related_name='video_audio',
            verbose_name=_("audio languages"))
    subtitles = models.ManyToManyField(Language, blank=True, related_name='video_subtitle',
            verbose_name=_("subtitle languages"))
    # TODO: Attachments generic relation
