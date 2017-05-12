from django.apps import AppConfig

from modeltranslation.translator import translator, NotRegistered
from watson import search as watson


class MaterialSearchAdapter(watson.SearchAdapter):
    """
    Dumps all translated titles and descriptions into the search index.
    The original fields to be translated are excluded.
    The translated fields are stored as metadata.
    """

    @property
    def translation_options(self):
        try:
            return translator.get_options_for_model(self.model)
        except NotRegistered:
            return None

    @property
    def exclude(self):
        if self.translation_options is None:
            return ()
        return self.translation_options.get_field_names()

    @property
    def store(self):
        if self.translation_options is None:
            return ()
        tss = self.translation_options.fields.values()
        return [t.name for ts in tss for t in ts]

    def _resolve_field(self, obj, field):
        content = super()._resolve_field(obj, field)
        # CharFields that get left blank can be represented by None -- annoying
        return '' if content is None else content

    def _join_translations(self, obj, field):
        if self.translation_options is None:
            content = self._resolve_field(obj, field)
        else:
            fs = self.translation_options.fields.get(field, set())
            content = ' '.join((self._resolve_field(obj, f.name) for f in fs))
        return self.prepare_content(content)

    def get_title(self, obj):
        return self._join_translations(obj, 'title')

    def get_description(self, obj):
        return self._join_translations(obj, 'brief')


class MaterialConfig(AppConfig):
    name = 'tk.material'

    def ready(self):
        for material in ['Activity', 'Video', 'Reading', 'Link']:
            model = self.get_model(material)
            watson.register(model.objects.approved(), MaterialSearchAdapter)
