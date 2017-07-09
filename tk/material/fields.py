from itertools import tee, filterfalse
from operator import itemgetter

from django import forms
from django.conf import global_settings
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _

from localized_fields.fields import LocalizedTextField, LocalizedUniqueSlugField

from .formfields import LocalizedMarkdownxFormField


class LocalizedMarkdownxTextField(LocalizedTextField):
    def formfield(self, **kwargs):
        defaults = {'form_class': LocalizedMarkdownxFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


# Stolen from https://gist.github.com/danni/f55c4ce19598b2b345ef

class LanguageField(ArrayField):
    def __init__(self, *args, **kwargs):
        self.limit_to = kwargs.pop('limit_to', [])
        self.prioritize = kwargs.pop('prioritize', [])
        defaults = {'base_field': CharField(max_length=7)}
        defaults.update(kwargs)
        return super().__init__(*args, **defaults)

    def get_languages(self):
        ls = ((c, _(n)) for (c, n) in global_settings.LANGUAGES)
        if self.limit_to:
            ls = ((c, n) for (c, n) in ls if c in self.limit_to)
        ls = sorted(ls, key=itemgetter(1))
        if self.prioritize:
            pred = lambda l: l[0] in self.prioritize
            lst, lsf = tee(ls)
            ls = list(filter(pred, lst)) + list(filterfalse(pred, lsf))
        return ls

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.get_languages()
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't care for it.
        return super(ArrayField, self).formfield(**defaults)
