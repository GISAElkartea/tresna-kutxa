from django.conf import settings
from django.forms.widgets import NumberInput, MultiWidget, CheckboxSelectMultiple

from localized_fields.widgets import LocalizedFieldWidget, AdminLocalizedFieldWidget
from markdownx.widgets import MarkdownxWidget, AdminMarkdownxWidget
from sass_processor.processor import sass_processor


class ToggleAllCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = 'toggle_all_checkbox_select_multiple.html'


class LocalizedMarkdownxWidget(LocalizedFieldWidget):
    template_name = 'localized_fields/multiwidget.html'
    widget = MarkdownxWidget


class AdminLocalizedMarkdownxWidget(AdminLocalizedFieldWidget):
    widget = AdminMarkdownxWidget


class NumberRangeInput(NumberInput):
    input_type = 'range'


# https://jsfiddle.net/simplgy/z93s82xL/
class RangeWidget(MultiWidget):
    template_name = 'material/range_widget.html'

    class Media:
        css = {'all': [sass_processor('sass/range_widget.sass')]}
        # JS loaded from within the template

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        super().__init__([
            NumberRangeInput(attrs={'min': attrs.pop('min', None)}),
            NumberRangeInput(attrs={'max': attrs.pop('max', None)}),
        ], attrs)

    def decompress(self, value):
        if value:
            return (value.lower, value.upper)
        return (None, None)
