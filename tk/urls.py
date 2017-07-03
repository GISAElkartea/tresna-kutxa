from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView

from .admin import tkadmin


localized = [
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='frontpage'),
    url(r'^material/', include('tk.material.urls')),
]


urlpatterns = i18n_patterns(*localized) + [
    url(r'^admin/', tkadmin.urls),
    url(r'^markdownx/', include('markdownx.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
