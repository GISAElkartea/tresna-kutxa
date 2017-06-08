from localized_fields.forms import LocalizedFieldForm
from localized_fields.widgets import LocalizedFieldWidget, AdminLocalizedFieldWidget
from markdownx.widgets import MarkdownxWidget, AdminMarkdownxWidget


class LocalizedMarkdownxWidget(LocalizedFieldWidget):
    widget = MarkdownxWidget


class LocalizedMarkdownxFormField(LocalizedFieldForm):
    widget = LocalizedMarkdownxWidget


class AdminLocalizedMarkdownxWidget(AdminLocalizedFieldWidget):
    widget = AdminMarkdownxWidget
