from functools import reduce
from operator import add

from django.urls import reverse
from django.http import HttpResponseNotAllowed
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers

from .filtersets import *
from .forms import ActivityForm, VideoForm, ReadingForm, LinkForm
from .models import Material, Activity, Video, Reading, Link


def tab_context(tabs):
    return {
        'tabs' : tabs,
        'media': reduce(add, [ form.media for name, url, form in tabs if form is not None ])
    }


def update_form(tabs, updated_form):
    return [(name, url, updated_form if updated_form.prefix == form.prefix else form)
            for (name, url, form) in tabs]

def search_tabs(request):
    material_filter = MaterialFilterSet(request.GET, prefix='material')
    activity_filter = ActivityFilterSet(request.GET, prefix='activity')
    reading_filter = ReadingFilterSet(request.GET, prefix='reading')
    video_filter = VideoFilterSet(request.GET, prefix='video')
    link_filter = LinkFilterSet(request.GET, prefix='link')
    return [
        (_('All material'), reverse('material:search-material'), material_filter.form),
        (_('Activities'), reverse('material:search-activity'), activity_filter.form),
        (_('Readings'), reverse('material:search-reading'), reading_filter.form),
        (_('Videos'), reverse('material:search-video'), video_filter.form),
        (_('Links'), reverse('material:search-link'), link_filter.form),
    ]


class BaseSubmitMaterial(CreateView):
    template_name = 'material/submit.html'

    def get_tabs(self):
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

    def get_context_data(self, *args, **kwargs):
        kwargs['submit_tabs'] = tab_context(update_form(self.get_tabs(), self.get_form()))
        kwargs['search_tabs'] = tab_context(search_tabs(self.request))
        return super().get_context_data(*args, **kwargs)


class SubmitMaterial(BaseSubmitMaterial):
    model = Material
    fields = []

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


class BaseDetail(LocalizedSlugMixin, DetailView):
    def get_context_data(self, *args, **kwargs):
        kwargs['search_tabs'] = tab_context(search_tabs(self.request))
        return super().get_context_data(*args, **kwargs)

    def get_template_names(self):
        try:
            if not self.object.approval.approved:
                return ['material/pending.html']
        except Material.approval.RelatedObjectDoesNotExist:
            pass
        return super().get_template_names()


class DetailActivity(BaseDetail):
    model = Activity


class DetailVideo(BaseDetail):
    model = Video


class DetailReading(BaseDetail):
    model = Reading


class DetailLink(BaseDetail):
    model = Link


class SingleModelSearch(ListView):
    prefix = None
    filterset_class = None
    paginate_by = 20

    @method_decorator(vary_on_headers('X-Requested-With'))
    def __call__(self, request, **kwargs):
        super().__call__(request, **kwargs)

    def get_template_names(self):
        if self.request.is_ajax():
            return ['material/search_ajax.html']
        return ['material/search.html']

    def get_tabs(self):
        material_filter = MaterialFilterSet(self.request.GET, prefix='material')
        activity_filter = ActivityFilterSet(self.request.GET, prefix='activity')
        reading_filter = ReadingFilterSet(self.request.GET, prefix='reading')
        video_filter = VideoFilterSet(self.request.GET, prefix='video')
        link_filter = LinkFilterSet(self.request.GET, prefix='link')
        return [
            (_('All material'), reverse('material:search-material'), material_filter.form),
            (_('Activities'), reverse('material:search-activity'), activity_filter.form),
            (_('Readings'), reverse('material:search-reading'), reading_filter.form),
            (_('Videos'), reverse('material:search-video'), video_filter.form),
            (_('Links'), reverse('material:search-link'), link_filter.form),
            ]

    def get_context_data(self, *args, **kwargs):
        kwargs['show_welcome'] = not self.request.GET
        kwargs['search_tabs'] = tab_context(update_form(self.get_tabs(), self.get_filterset().form))
        return super().get_context_data(*args, **kwargs)

    def get_filterset(self):
        return self.filterset_class(
                self.request.GET,
                queryset=self.queryset,
                prefix=self.prefix)

    def get_queryset(self):
        filterset = self.get_filterset()
        query = self.request.GET.get('q')
        if not query:
            return filterset.qs
        return filterset.qs.search(query)

class SearchMaterial(SingleModelSearch):
    queryset = Material.objects.approved()
    filterset_class = MaterialFilterSet
    prefix = 'material'

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
