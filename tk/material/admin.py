from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .models import (Subject, Goal, GroupFeature, Location, Language,
                     Approval, Activity, Reading, Video, Link)


# TODO: Do not delete related
admin.register(Subject, Goal, GroupFeature, Location, Language)(TranslationAdmin)


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    # TODO: Delete related material action
    # TODO: Approve action or button?
    # TODO: Limit content types to material subclasses
    # TODO: No add view
    list_filter = ['content_type', 'requested', 'published', 'approved']
    list_display = ['__str__', 'content_object', 'requested', 'email',
                    'approved', 'published']
    fields = [('requested', 'email'), ('published', 'approved'),
              'content_object', 'comment']
    readonly_fields = ['requested', 'published', 'email', 'content_object']

    def content_object(self, obj):
        view = '{}_{}_change'.format(obj.content_type.app_label, obj.content_type.model)
        return format_html('<a href="{}">{}</a>', reverse(view), str(obj.content_object))
    content_object.short_description = _("content object")


@admin.register(Activity)
class ActivityAdmin(TranslationAdmin):
    fieldsets = [
            (_("Classification"), {
                'fields': ['goals', 'subject']}),
            (_("Conditions"), {
                'fields': [('min_people', 'max_people'),
                           'location',
                           'duration',
                           'group_feature']}),
            (_("Content"), {
                'fields': ['author', 'title', 'link', 'brief', 'notes', 'attachment']})
            ]
    filter_horizontal = ['goals']
    list_filter = ['min_people', 'max_people', 'location', 'duration',
                   'group_feature', 'goals', 'subject']
    list_display = ['__str__', 'approval']
    search_fields = ['title', 'brief', 'notes']


@admin.register(Reading)
class ReadingAdmin(TranslationAdmin):
    fieldsets = [
            (_("Details"), {
                'fields': ['pages',
                           'year',
                           'language',
                           'subject']}),
            (_("Content"), {
                'fields': ['author', 'title', 'link', 'brief', 'attachment']})
            ]
    list_filter = ['pages', 'year', 'language', 'subject']
    list_display = ['__str__', 'approval']
    search_fields = ['title', 'brief']


@admin.register(Video)
class VideoAdmin(TranslationAdmin):
    fieldsets = [
            (_("Details"), {
                'fields': ['duration',
                           'year',
                           'audios',
                           'subtitles',
                           'subject']}),
            (_("Content"), {
                'fields': ['author', 'title', 'link', 'brief', 'attachment']})
            ]
    filter_horizontal = ['audios', 'subtitles']
    list_filter = ['duration', 'year', 'audios', 'subtitles', 'subject']
    list_display = ['__str__', 'approval']
    search_fields = ['title', 'brief']


@admin.register(Link)
class LinkAdmin(TranslationAdmin):
    fieldsets = [
            (_("Details"), {
                'fields': ['subject']}),
            (_("Content"), {
                'fields': ['author', 'title', 'link', 'brief']})
            ]
    list_filter = ['subject']
    list_display = ['__str__', 'approval']
    search_fields = ['title', 'brief']
