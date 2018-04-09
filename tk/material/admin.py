from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from markdownx.admin import MarkdownxModelAdmin
from localized_fields.admin import LocalizedFieldsAdminMixin

from .formfields import AdminLocalizedMarkdownxWidget


class LocalizedAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    pass


class ApprovalAdmin(admin.ModelAdmin):
    # TODO: Delete related material action
    # TODO: Approve action or button?
    list_filter = ['timestamp', 'approved']
    list_display = ['__str__', 'timestamp', 'email', 'approved']
    fields = [('timestamp', 'email'), 'approved', 'material_link', 'comment']
    readonly_fields = ['timestamp', 'email', 'material_link']

    def has_add_permission(self, request, obj=None):
        return False

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


class MaterialAdmin(MarkdownxModelAdmin, LocalizedFieldsAdminMixin, admin.ModelAdmin):
    def approval_link(self, material_obj):
        name = 'admin:material_approval_change'
        return format_html('<a href="{}">{}</a>'.format(
            reverse(name, args=[material_obj.approval.pk]),
            material_obj.approval))
    approval_link.short_description = _('Approval')


class ActivityAdmin(MaterialAdmin):
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
    list_filter = ['min_people', 'max_people', 'location', 'duration',
                   'group_feature', 'goals', 'subject']
    list_display = ['__str__', 'timestamp', 'approval_link']
    readonly_fields = ['approval_link']
    search_fields = ['title', 'brief', 'notes']


class ReadingAdmin(MaterialAdmin):
    fieldsets = [
            (_("State"), {
                'fields': ['approval_link',
                           # TODO: Creation time
                           ]}),
            (_("Classification"), {
                'fields': ['pages',
                           'year',
                           'languages',
                           'subject']}),
            (_("Content"), {
                'fields': ['author', 'title', 'url', 'brief', 'attachment']})
            ]
    readonly_fields = ['approval_link']
    list_filter = ['pages', 'year', 'languages', 'subject']
    list_display = ['__str__', 'timestamp', 'approval_link']
    search_fields = ['title', 'brief']


class VideoAdmin(MaterialAdmin):
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
    list_filter = ['duration', 'year', 'audios', 'subtitles', 'subject']
    list_display = ['__str__', 'timestamp', 'approval_link']
    search_fields = ['title', 'brief']


class LinkAdmin(MaterialAdmin):
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
    list_display = ['__str__', 'timestamp', 'approval_link']
    search_fields = ['title', 'brief']
