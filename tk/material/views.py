from functools import reduce
from operator import add

from django.urls import reverse
from django.http import HttpResponseNotAllowed
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.utils.translation import ugettext as _

from watson import search
from watson.views import SearchMixin as WatsonSearchView

from .filtersets import *
from .forms import ActivityForm, VideoForm, ReadingForm, LinkForm
from .models import Material, Activity, Video, Reading, Link


class TabbedMixin:
    def get_tabs(self):
        return []

    def get_context_data(self, **kwargs):
        tabs = self.get_tabs()
        kwargs['tabs'] = tabs
        # Union of all media files
        kwargs['tab_media'] = reduce(add, [ form.media
                                            for name, url, form in tabs
                                            if form is not None ])
        return super().get_context_data(**kwargs)

class BaseSubmitMaterial(TabbedMixin, CreateView):
    template_name = 'material/submit.html'

    def get_base_tabs(self):
        return [
            (_('Activity'), reverse('material:submit-activity'),
                ActivityForm(prefix='activity')),
            (_('Reading'), reverse('material:submit-reading'),
                ReadingForm(prefix='reading')),
            (_('Video'), reverse('material:submit-video'),
                VideoForm(prefix='video')),
            (_('Link'), reverse('material:submit-link'),
                LinkForm(prefix='link')),
        ]

    def get_tabs(self):
        current = self.get_form()
        return [ (name, url, current if current.prefix == form.prefix else form)
                 for name, url, form in self.get_base_tabs() ]


class SubmitMaterial(BaseSubmitMaterial):
    def post(self, *args, **kwargs):
        return HttpResponseNotAllowed(['GET'])


class SubmitActivity(BaseSubmitMaterial):
    prefix = 'activity'
    model = Activity
    form_class = ActivityForm


class SubmitReading(BaseSubmitMaterial):
    prefix = 'reading'
    model = Reading
    form_class = ReadingForm


class SubmitVideo(BaseSubmitMaterial):
    prefix = 'video'
    model = Video
    form_class = VideoForm


class SubmitLink(BaseSubmitMaterial):
    prefix = 'link'
    model = Link
    form_class = LinkForm


class LocalizedSlugMixin(SingleObjectMixin):
    def get_slug_field(self):
        slug_field = super().get_slug_field()
        lang_code = getattr(self.request, 'LANGUAGE_CODE', None)
        if lang_code is not None:
            return '{}__{}'.format(slug_field, lang_code)
        return slug_field


class PendingApprovalMixin():
    def get_template_names(self):
        if not self.object.approval.approved:
            return ['material/pending.html']
        return super().get_template_names()


class DetailActivity(LocalizedSlugMixin, PendingApprovalMixin, DetailView):
    model = Activity


class DetailVideo(LocalizedSlugMixin, PendingApprovalMixin, DetailView):
    model = Video


class DetailReading(LocalizedSlugMixin, PendingApprovalMixin, DetailView):
    model = Reading


class DetailLink(LocalizedSlugMixin, PendingApprovalMixin, DetailView):
    model = Link


class SearchMaterial(TabbedMixin, WatsonSearchView, ListView):
    template_name = 'material/search.html'

    def get_tabs(self):
        activity_filter = ActivityFilterSet(self.request.GET, prefix='activity')
        reading_filter = ReadingFilterSet(self.request.GET, prefix='reading')
        video_filter = VideoFilterSet(self.request.GET, prefix='video')
        link_filter = LinkFilterSet(self.request.GET, prefix='link')
        return [
            (_('All material'), reverse('material:search-material'), None),
            (_('Activities'), reverse('material:search-activity'), activity_filter.form),
            (_('Readings'), reverse('material:search-reading'), reading_filter.form),
            (_('Videos'), reverse('material:search-video'), video_filter.form),
            (_('Links'), reverse('material:search-link'), link_filter.form),
        ]


class SingleModelSearch(SearchMaterial):
    prefix = None
    filterset_class = None

    def get_context_data(self, *args, **kwargs):
        kwargs['form'] = self.filterset_class(self.request.GET).form
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self):
        filterset = self.filterset_class(
                self.request.GET,
                queryset=self.queryset,
                prefix=self.prefix)
        return search.filter(filterset.qs, self.query)

    def get_queryset(self):
        if not self.get_query(self.request):
            return self.queryset
        return super().get_queryset()

class SearchActivity(SingleModelSearch):
    queryset = Activity.objects.approved()
    filterset_class = ActivityFilterSet
    prefix = 'activity'

class SearchVideo(SingleModelSearch):
    queryset = Video.objects.approved()
    filterset_class = VideoFilterSet
    prefix = 'video'

class SearchLink(SingleModelSearch):
    queryset = Link.objects.approved()
    filterset_class = LinkFilterSet
    prefix = 'link'

class SearchReading(SingleModelSearch):
    queryset = Reading.objects.approved()
    filterset_class = ReadingFilterSet
    prefix = 'reading'
