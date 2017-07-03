from django.core.urlresolvers import reverse, resolve
from django.template import Library
from django.utils import translation
from django.templatetags.i18n import register


@register.simple_tag(takes_context=True)
def translate_url(context, language):
    view = resolve(context['request'].path)
    args = [a for a in view.args if a is not None]
    kwargs = {k:v for k,v in view.kwargs.items() if v is not None}
    with translation.override(language):
        url = reverse(view.view_name, args=args, kwargs=kwargs)
    return url
