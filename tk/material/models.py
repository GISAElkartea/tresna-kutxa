import datetime

from django.db import models
from django.db.models import Subquery, Q
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

    code = models.CharField(primary_key=True, max_length=16, verbose_name=_("code"))
    name = models.CharField(max_length=512, verbose_name=_("name"))
    # TODO: Prepopulate
    # TODO: Autocomplete search interface

    def __str__(self):
        return self.name


class Approval(models.Model):
    class Meta:
        verbose_name = _("Approval")
        verbose_name_plural = _("Approvals")

    resource = models.ForeignKey('ApprovalResource', on_delete=models.CASCADE, verbose_name=_("resource"))

    # TODO: Hide in forms
    requested = models.DateTimeField(auto_now_add=True, verbose_name=_("created on"))
    published = models.DateTimeField(null=True, blank=True, verbose_name=_("published on"))
    approved = models.BooleanField(default=False, verbose_name=_("is approved"))
    comment = models.TextField(blank=True, verbose_name=_("comment"))
    email = models.EmailField(blank=True, verbose_name=_("contact email"))

    def __str__(self):
        return str(self.resource)


class ApprovalResource(models.Model):
    activity = models.OneToOneField('Activity', null=True, blank=True, on_delete=models.CASCADE)
    video = models.OneToOneField('Video', null=True, blank=True, on_delete=models.CASCADE)
    reading = models.OneToOneField('Reading', null=True, blank=True, on_delete=models.CASCADE)
    link = models.OneToOneField('Link', null=True, blank=True, on_delete=models.CASCADE)

    @property
    def resource(self):
        if self.activity is not None:
            return self.activity
        if self.video is not None:
            return self.video
        if self.reading is not None:
            return self.reading
        if self.link is not None:
            return self.link
        return None

    def __str__(self):
        if self.activity is not None:
            return _("Activity {}").format(self.activity)
        if self.video is not None:
            return _("Video {}").format(self.video)
        if self.reading is not None:
            return _("Reading {}").format(self.reading)
        if self.link is not None:
            return _("Link {}").format(self.link)
        return super().__str__()


class ApprovedQuerySet(models.QuerySet):
    def approved(self):
        bypassed = Q(approvalresource__isnull=True)
        approved = Q(approvalresource__approval__approved=True)
        return self.filter(bypassed | approved)

    def unapproved(self):
        return self.filter(approvalresource__approval__approved=False)


class Material(models.Model):
    APPROVAL_RESOURCE_KEY = ''

    class Meta:
        abstract = True

    title = models.CharField(max_length=512, verbose_name=_("title"))
    slug = AutoSlugField(populate_from='title', unique=True)

    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name=_("subject"))
    brief = models.TextField(blank=True, verbose_name=_("brief"))
    author = models.CharField(max_length=512, blank=True, verbose_name=_("author"))
    link = models.URLField(blank=True, verbose_name=_("link"),
            help_text=_("Link the material if its copyright does not allow sharing it."))

    # TODO
    @property
    def approval(self):
        link = 'resource__{}'.format(APPROVAL_RESOURCE_KEY)
        try:
            return Approval.objects.get(**{link: self})
        except Approval.DoesNotExist:
            return None

    def __str__(self):
        return self.title


class Activity(Material):
    APPROVAL_RESOURCE_KEY = 'activity'
    objects = ApprovedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    subject = models.ForeignKey(Subject, null=True, blank=True,
            on_delete=models.SET_NULL, verbose_name=_("subject"))
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
    notes = models.TextField(blank=True, verbose_name=_("notes"))
    attachment = models.FileField(upload_to='material/activities/', blank=True,
            verbose_name=_("attachment"))

    def clean(self):
        if self.min_people > self.max_people:
            raise ValidationError(_("The upper bound for the people involved "
                "in the activity cannot be less than the lower bound."))

def validate_year(year):
    if datetime.date.today().year < year:
        raise ValidationError(_("That year is still in the future."))


class Reading(Material):
    APPROVAL_RESOURCE_KEY = 'reading'
    objects = ApprovedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Reading")
        verbose_name_plural = _("Readings")

    pages = models.PositiveIntegerField(verbose_name=_("pages"))
    year = models.PositiveIntegerField(validators=[validate_year], verbose_name=_("year"))
    language = models.ForeignKey(Language, on_delete=models.PROTECT, verbose_name=_("language"))
    attachment = models.FileField(upload_to='material/readings/', blank=True,
            verbose_name=_("attachment"))


class Video(Material):
    APPROVAL_RESOURCE_KEY = 'video'
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
    attachment = models.FileField(upload_to='material/videos', blank=True,
            verbose_name=_("attachment"))


class Link(Material):
    APPROVAL_RESOURCE_KEY = 'link'
    objects = ApprovedQuerySet.as_manager()

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    link = models.URLField(verbose_name=_("link"))
