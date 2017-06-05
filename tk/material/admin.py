from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from modeltranslation.admin import TranslationAdmin

from .models import (Subject, Goal, GroupFeature, Location, Language,
                     Approval, Material, Activity, Reading, Video, Link)


# TODO: Do not delete related
admin.register(Subject, Goal, GroupFeature, Location, Language)(TranslationAdmin)


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    # TODO: Delete related material action
    # TODO: Approve action or button?
    # TODO: No add view
    list_filter = ['requested', 'approved']
    list_display = ['__str__', 'requested', 'email', 'approved']
    fields = [('requested', 'email'), 'approved', 'material_link', 'comment']
    readonly_fields = ['requested', 'email', 'material_link']

    def material_link(self, approval_obj):
        for material_type in ['activity', 'video', 'reading', 'link']:
            name = 'admin:material_{}_change'.format(material_type)
            try:
                obj = getattr(approval_obj.material, material_type)
            except ObjectDoesNotExist:
                pass
            else:
                return format_html('<a href="{}">{}</a>', reverse(name,
                    args=[obj.pk]), obj)
    material_link.short_description = _('Material')


class MaterialTypeMixin():
    def approval_link(self, material_obj):
        name = 'admin:material_approval_change'
        return format_html('<a href="{}">{}</a>'.format(
            reverse(name, args=[material_obj.approval.pk]),
            material_obj.approval))
    approval_link.short_description = _('Approval')


@admin.register(Activity)
class ActivityAdmin(TranslationAdmin, MaterialTypeMixin):
    fieldsets = [
            (_("State"), {
                'fields': ['approval_link',
                           # TODO: Creation time
                           ]}),
            (_("Classification"), {
                'fields': ['goals',
                           'subject',
                           ('min_people', 'max_people'),
                           'location',
                           'duration',
                           'group_feature']}),
            (_("Content"), {
                'fields': ['author', 'title', 'url', 'brief', 'notes', 'attachment']})
            ]
    filter_horizontal = ['goals']
    list_filter = ['min_people', 'max_people', 'location', 'duration',
                   'group_feature', 'goals', 'subject']
    list_display = ['__str__', 'approval_link']
    readonly_fields = ['approval_link']
    search_fields = ['title', 'brief', 'notes']


@admin.register(Reading)
class ReadingAdmin(TranslationAdmin, MaterialTypeMixin):
    fieldsets = [
            (_("State"), {
                'fields': ['approval_link',
                           # TODO: Creation time
                           ]}),
            (_("Classification"), {
                'fields': ['pages',
                           'year',
                           'language',
                           'subject']}),
            (_("Content"), {
                'fields': ['author', 'title', 'url', 'brief', 'attachment']})
            ]
    readonly_fields = ['approval_link']
    list_filter = ['pages', 'year', 'language', 'subject']
    list_display = ['__str__', 'approval_link']
    search_fields = ['title', 'brief']


@admin.register(Video)
class VideoAdmin(TranslationAdmin, MaterialTypeMixin):
    fieldsets = [
            (_("State"), {
                'fields': ['approval_link',
                           # TODO: Creation time
                           ]}),
            (_("Classification"), {
                'fields': ['duration',
                           'year',
                           'audios',
                           'subtitles',
                           'subject']}),
            (_("Content"), {
                'fields': ['author', 'title', 'url', 'brief', 'attachment']})
            ]
    readonly_fields = ['approval_link']
    filter_horizontal = ['audios', 'subtitles']
    list_filter = ['duration', 'year', 'audios', 'subtitles', 'subject']
    list_display = ['__str__', 'approval_link']
    search_fields = ['title', 'brief']


@admin.register(Link)
class LinkAdmin(TranslationAdmin, MaterialTypeMixin):
    fieldsets = [
            (_("State"), {
                'fields': ['approval_link',
                           # TODO: Creation time
                           ]}),
            (_("Classification"), {
                'fields': ['subject']}),
            (_("Content"), {
                'fields': ['author', 'title', 'url', 'brief']})
            ]
    readonly_fields = ['approval_link']
    list_filter = ['subject']
    list_display = ['__str__', 'approval_link']
    search_fields = ['title', 'brief']
