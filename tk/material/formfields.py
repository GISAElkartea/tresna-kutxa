from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings

from localized_fields.forms import LocalizedFieldForm
from localized_fields.widgets import LocalizedFieldWidget, AdminLocalizedFieldWidget
from markdownx.widgets import MarkdownxWidget, AdminMarkdownxWidget


class LocalizedMarkdownxWidget(LocalizedFieldWidget):
    widget = MarkdownxWidget


class AdminLocalizedMarkdownxWidget(AdminLocalizedFieldWidget):
    widget = AdminMarkdownxWidget


class LocalizedMarkdownxFormField(LocalizedFieldForm):
    widget = LocalizedMarkdownxWidget
