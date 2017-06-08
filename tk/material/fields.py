from django import forms
from django.conf import global_settings
from django.contrib.postgres.fields import ArrayField
from django.db.models import CharField

from localized_fields.fields import LocalizedField

from .formfields import LocalizedMarkdownxFormField


class LocalizedMarkdownxField(LocalizedField):
    def formfield(self, **kwargs):
        defaults = {'form_class': LocalizedMarkdownxFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


# Stolen from https://gist.github.com/danni/f55c4ce19598b2b345ef

class LanguageField(ArrayField):
    def __init__(self, *args, **kwargs):
        defaults = {'base_field': CharField(max_length=7)}
        defaults.update(kwargs)
        return super().__init__(*args, **defaults)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': global_settings.LANGUAGES,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't care for it.
        return super(ArrayField, self).formfield(**defaults)
