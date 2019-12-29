from django.contrib import admin

from localized_fields.admin import LocalizedFieldsAdminMixin


class ChunkAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    fields = ["slug", "content"]
