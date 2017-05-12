from django.conf.urls import url, include

from .views import *

slug = r'(?P<slug>(\w|-)+)'

urlpatterns = [url('', include([
    url(r'^submit/activity/$', CreateActivity.as_view(), name='create-activity'),
    url(r'^submit/video/$', CreateVideo.as_view(), name='create-video'),
    url(r'^submit/reading/$', CreateReading.as_view(), name='create-reading'),
    url(r'^submit/link/$', CreateLink.as_view(), name='create-link'),

    url(r'^activity/{}/$'.format(slug), DetailActivity.as_view(), name='detail-activity'),
    url(r'^video/{}/$'.format(slug), DetailVideo.as_view(), name='detail-video'),
    url(r'^reading/{}/$'.format(slug), DetailReading.as_view(), name='detail-reading'),
    url(r'^link/{}/$'.format(slug), DetailLink.as_view(), name='detail-link'),

    ], namespace='material')),
]
