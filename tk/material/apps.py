from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils import translation
from django.conf import settings

from watson import search
from localized_fields.fields import LocalizedField


class MaterialSearchAdapter(search.SearchAdapter):
    """
    Dumps all translated titles and descriptions into the search index.
    The translated fields are stored as metadata.
    """

    @property
    def store(self):
        return ['title', 'urls', 'brief']

    def _join_translations(self, field: LocalizedField) -> str:
        return ' '.join([v for v in field.values() if v is not None])

    def get_title(self, obj):
        return self._join_translations(getattr(obj, 'title'))

    def get_description(self, obj):
        return self._join_translations(getattr(obj, 'brief'))

    def urls(self, obj):
        urls = {}
        for lang, _ in settings.LANGUAGES:
            with translation.override(lang):
                urls[lang] = obj.get_absolute_url()
        return urls

    def get_url(self, obj):
        # URLs are localized, cannot store in a text field
        return ''


class MaterialConfig(AppConfig):
    name = 'tk.material'

    def ready(self):
        for mn in ['Activity', 'Reading', 'Video', 'Link']:
            m = self.get_model(mn)
            search.register(m.objects.approved(), MaterialSearchAdapter)
