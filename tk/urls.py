from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView

from .admin import tkadmin


localized = [
    url(r'^', include('tk.material.urls')),
]


urlpatterns = i18n_patterns(*localized) + [
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', tkadmin.urls),
    url(r'^markdownx/', include('markdownx.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
