from django.conf.urls import url, include

from .views import *

slug = r'(?P<slug>(\w|-)+)'
mat_type = r'(?P<type>\w+)'

urlpatterns = [url('', include([
    url(r'^submit/(?:{}/)?$'.format(mat_type), CreateMaterial.as_view(), name='create-material'),

    url(r'^activity/{}/$'.format(slug), DetailActivity.as_view(), name='detail-activity'),
    url(r'^video/{}/$'.format(slug), DetailVideo.as_view(), name='detail-video'),
    url(r'^reading/{}/$'.format(slug), DetailReading.as_view(), name='detail-reading'),
    url(r'^link/{}/$'.format(slug), DetailLink.as_view(), name='detail-link'),

    ], namespace='material')),
]
