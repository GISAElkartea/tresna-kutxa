from django import forms
from django.conf import global_settings
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db.models import CharField
from django.utils.translation import ugettext as _

from localized_fields.fields import LocalizedField, LocalizedUniqueSlugField

from .formfields import AnyLocalizedMarkdownxFormField, AnyLocalizedFormField


class AnyLocalizedField(LocalizedField):
    """
    Validates that at least one language has been filled in if not null=True.
    The default language is no longer required.
    """

    def validate(self, value, *args):
        if self.null:
            return
        if all([not value.get(l) for l, lv in settings.LANGUAGES]):
            raise ValidationError(_("Supply at least one language"),
                    code='incomplete')

    def formfield(self, **kwargs):
        defaults = {'form_class': AnyLocalizedFormField,
                    'require_all_fields': False,
                    'required': True}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class AnyLocalizedMarkdownxField(AnyLocalizedField):
    def formfield(self, **kwargs):
        defaults = {'form_class': AnyLocalizedMarkdownxFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class AnyLocalizedUniqueSlugField(AnyLocalizedField, LocalizedUniqueSlugField):
    pass


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
