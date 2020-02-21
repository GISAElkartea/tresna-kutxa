from django.urls import reverse, resolve
from django.template import Library
from django.utils import translation
from django.templatetags.i18n import register


@register.simple_tag(takes_context=True)
def translate_url(context, language):
    if hasattr(context.get('object', None), 'get_absolute_url'):
        with translation.override(language):
            return context['object'].get_absolute_url()

    view = resolve(context['request'].path)
    args = [a for a in view.args if a is not None]
    kwargs = {k:v for k,v in view.kwargs.items() if v is not None}
    with translation.override(language):
        return reverse(view.view_name, args=args, kwargs=kwargs)


@register.filter
def paginate_url(page, request):
    params = request.GET.copy()
    params.setlist('page', [page])
    return params.urlencode()
