from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import IntegerRangeField

from localized_fields.admin import LocalizedFieldsAdminMixin
from localized_fields.fields import LocalizedTextField

from .widgets import AdminLocalizedMarkdownxWidget, RangeWidget


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


class MaterialAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    formfield_overrides = {
            LocalizedTextField: {'widget': AdminLocalizedMarkdownxWidget},
            }

    def approval_link(self, material_obj):
        name = 'admin:material_approval_change'
        return format_html('<a href="{}">{}</a>'.format(
            reverse(name, args=[material_obj.approval.pk]),
            material_obj.approval))
    approval_link.short_description = _('Approval')


class ActivityAdmin(MaterialAdmin):
    formfield_overrides = {
            LocalizedTextField: {'widget': AdminLocalizedMarkdownxWidget},
            IntegerRangeField: {'widget': RangeWidget},
            }

    fieldsets = [
            (_("State"), {
                'fields': ['approval_link',
                           # TODO: Creation time
                           ]}),
            (_("Classification"), {
                'fields': ['highlight',
                           'subjects',
                           'num_people',
                           'location',
                           'duration',
                           'group_feature']}),
            (_("Content"), {
                'fields': ['author', 'title', 'goal', 'url', 'brief', 'notes', 'attachment']})
            ]
    list_filter = ['highlight', 'location', 'group_feature', 'subjects']
    list_display = ['__str__', 'timestamp', 'approval_link', 'highlight', 'location', 'group_feature']
    list_editable = ['highlight', 'location', 'group_feature']
    readonly_fields = ['approval_link']
    search_fields = ['title', 'brief', 'notes']


class ReadingAdmin(MaterialAdmin):
    fieldsets = [
            (_("State"), {
                'fields': ['approval_link',
                           # TODO: Creation time
                           ]}),
            (_("Classification"), {
                'fields': ['highlight',
                           'pages',
                           'year',
                           'languages',
                           'subjects']}),
            (_("Content"), {
                'fields': ['author', 'title', 'goal', 'url', 'attachment', 'brief']})
            ]
    readonly_fields = ['approval_link']
    list_filter = ['highlight', 'pages', 'year', 'languages', 'subjects']
    list_display = ['__str__', 'timestamp', 'approval_link', 'highlight', 'pages', 'year']
    list_editable = ['highlight', 'pages', 'year']
    search_fields = ['title', 'brief']


class VideoAdmin(MaterialAdmin):
    fieldsets = [
            (_("State"), {
                'fields': ['approval_link',
                           # TODO: Creation time
                           ]}),
            (_("Classification"), {
                'fields': ['highlight',
                           'duration',
                           'year',
                           'audios',
                           'subtitles',
                           'subjects']}),
            (_("Content"), {
                'fields': ['author', 'title', 'goal', 'url', 'brief']})
            ]
    readonly_fields = ['approval_link']
    list_filter = ['highlight', 'year', 'audios', 'subtitles', 'subjects']
    list_display = ['__str__', 'timestamp', 'approval_link', 'highlight', 'year', ]
    list_editable = ['highlight', 'year']
    search_fields = ['title', 'brief']


class LinkAdmin(MaterialAdmin):
    fieldsets = [
            (_("State"), {
                'fields': ['approval_link',
                           # TODO: Creation time
                           ]}),
            (_("Classification"), {
                'fields': ['highlight', 'subjects']}),
            (_("Content"), {
                'fields': ['author', 'title', 'goal', 'url', 'brief']})
            ]
    readonly_fields = ['approval_link']
    list_filter = ['highlight', 'subjects']
    list_display = ['__str__', 'timestamp', 'approval_link', 'highlight']
    list_editable = ['highlight']
    search_fields = ['title', 'brief']
