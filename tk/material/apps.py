from django.apps import AppConfig

from watson import search as watson
from localized_fields.fields import LocalizedField

class MaterialSearchAdapter(watson.SearchAdapter):
    """
    Dumps all translated titles and descriptions into the search index.
    The translated fields are stored as metadata.
    """

    @property
    def store(self):
        return ['title', 'brief']

    def _join_translations(self, field: LocalizedField) -> str:
        return ' '.join(field.values())

    def get_title(self, obj):
        return self._join_translations(getattr(obj, 'title'))

    def get_description(self, obj):
        return self._join_translations(getattr(obj, 'brief'))


class MaterialConfig(AppConfig):
    name = 'tk.material'

    def ready(self):
        # All material types related one-to-one to their Material parent.
        # This parent contains all information which is meaningful to search.
        Material = self.get_model('Material')
        watson.register(Material.objects.approved(), MaterialSearchAdapter)
