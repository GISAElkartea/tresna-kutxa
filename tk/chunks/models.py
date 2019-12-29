import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from localized_fields.fields import LocalizedTextField


class Chunk(models.Model):
    class Meta:
        ordering = ['slug']
        verbose_name = _("Chunk")
        verbose_name_plural = _("Chunks")

    slug = models.SlugField(unique=True, verbose_name=_("slug"))
    content = LocalizedTextField(blank=False, null=False, required=False, verbose_name=_("content"))

    def __str__(self):
        return str(self.slug)
