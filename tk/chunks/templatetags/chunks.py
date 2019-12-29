from django import template
from django.utils.safestring import mark_safe

from tk.chunks.models import Chunk

register = template.Library()

@register.simple_tag
def chunk(slug):
    return mark_safe(Chunk.objects.get(slug=slug).content)
