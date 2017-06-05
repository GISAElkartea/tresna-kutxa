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
    # TODO: No add view
    list_filter = ['requested', 'published', 'approved']
    list_display = ['__str__', 'requested', 'email', 'approved', 'published']
    fields = [('requested', 'email'), ('published', 'approved'),
              'material', 'comment']
    readonly_fields = ['requested', 'published', 'email', 'material']


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
                'fields': ['author', 'title', 'url', 'brief', 'notes', 'attachment']})
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
                'fields': ['author', 'title', 'url', 'brief', 'attachment']})
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
                'fields': ['author', 'title', 'url', 'brief', 'attachment']})
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
                'fields': ['author', 'title', 'url', 'brief']})
            ]
    list_filter = ['subject']
    list_display = ['__str__', 'approval']
    search_fields = ['title', 'brief']
