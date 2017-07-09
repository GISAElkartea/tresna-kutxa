from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings

from localized_fields.forms import LocalizedFieldForm
from localized_fields.widgets import LocalizedFieldWidget, AdminLocalizedFieldWidget
from markdownx.widgets import MarkdownxWidget, AdminMarkdownxWidget


class LocalizedMarkdownxWidget(LocalizedFieldWidget):
    template_name = 'localized_fields/multiwidget.html'
    widget = MarkdownxWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for ((lc, ln), w) in zip(settings.LANGUAGES, self.widgets):
            w.attrs['lang_code'] = lc
            w.attrs['lang_name'] = ln


class AdminLocalizedMarkdownxWidget(AdminLocalizedFieldWidget):
    widget = AdminMarkdownxWidget


class LocalizedMarkdownxFormField(LocalizedFieldForm):
    widget = LocalizedMarkdownxWidget
