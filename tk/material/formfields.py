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


class AnyLocalizedFormField(LocalizedFieldForm):
    def __init__(self, *args, **kwargs):
        fields = []

        for lang_code, _ in settings.LANGUAGES:
            field_options = {'required': False, 'label': lang_code}
            fields.append(forms.fields.CharField(**field_options))

        # Shortcircuit LocalizedFieldForm.__init__
        super(LocalizedFieldForm, self).__init__(fields, *args, **kwargs)

        # Set 'required' attribute for each widget separately
        for f, w in zip(self.fields, self.widget.widgets):
            w.is_required = f.required


class AnyLocalizedMarkdownxFormField(AnyLocalizedFormField):
    widget = LocalizedMarkdownxWidget
