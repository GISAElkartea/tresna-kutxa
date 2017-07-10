from django.apps import AppConfig
from django.db.models.signals import post_save

from watson import search
from localized_fields.fields import LocalizedField


class MaterialSearchAdapter(search.SearchAdapter):
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


def update_material_index(sender, instance, **kwargs):
    search.default_search_engine.update_obj_index(instance.material_ptr)


class MaterialConfig(AppConfig):
    name = 'tk.material'

    def ready(self):
        # All material types related one-to-one to their Material parent.
        # This parent contains all information that is meaningful to search.
        Material = self.get_model('Material')
        search.register(Material.objects.approved(), MaterialSearchAdapter)

        for m in ['Activity', 'Reading', 'Video', 'Link']:
            post_save.connect(update_material_index, sender=self.get_model(m))
