from django.conf.urls import url, include

from .views import *

slug = r'(?P<slug>(\w|-)+)'
mat_type = r'(?P<type>\w+)'

app_name = 'material'
urlpatterns = [
    url(r'^$', SearchMaterial.as_view(), name='search-material'),
    url(r'^activity/$', SearchActivity.as_view(), name='search-activity'),
    url(r'^video/$', SearchVideo.as_view(), name='search-video'),
    url(r'^reading/$', SearchReading.as_view(), name='search-reading'),
    url(r'^link/$', SearchLink.as_view(), name='search-link'),

    url(r'^submit/material/$', SubmitActivity.as_view(), name='submit-material'),
    url(r'^submit/activity/$', SubmitActivity.as_view(), name='submit-activity'),
    url(r'^submit/video/$', SubmitVideo.as_view(), name='submit-video'),
    url(r'^submit/reading/$', SubmitReading.as_view(), name='submit-reading'),
    url(r'^submit/link/$', SubmitLink.as_view(), name='submit-link'),

    url(r'^detail/activity/{}/$'.format(slug), DetailActivity.as_view(), name='detail-activity'),
    url(r'^detail/video/{}/$'.format(slug), DetailVideo.as_view(), name='detail-video'),
    url(r'^detail/reading/{}/$'.format(slug), DetailReading.as_view(), name='detail-reading'),
    url(r'^detail/link/{}/$'.format(slug), DetailLink.as_view(), name='detail-link'),
]
