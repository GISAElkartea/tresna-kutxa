from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
        url(r'^material/', include('tk.material.urls')),
        url(r'^admin/', admin.site.urls),
]
