from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

from .admin import tkadmin

urlpatterns = [
        url(r'^$', TemplateView.as_view(template_name='base.html'), name='frontpage'),

        url(r'^material/', include('tk.material.urls')),

        url(r'^admin/', tkadmin.urls),
        url(r'^markdownx/', include('markdownx.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
