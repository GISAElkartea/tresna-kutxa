from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView


urlpatterns = [
        url(r'^$', TemplateView.as_view(template_name='base.html'), name='frontpage'),

        url(r'^material/', include('tk.material.urls')),
        url(r'^admin/', admin.site.urls),
]
