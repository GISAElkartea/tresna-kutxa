from django.conf import settings

from localized_fields.widgets import LocalizedFieldWidget, AdminLocalizedFieldWidget
from markdownx.widgets import MarkdownxWidget, AdminMarkdownxWidget


class LocalizedMarkdownxWidget(LocalizedFieldWidget):
    template_name = 'localized_fields/multiwidget.html'
    widget = MarkdownxWidget


class AdminLocalizedMarkdownxWidget(AdminLocalizedFieldWidget):
    widget = AdminMarkdownxWidget
