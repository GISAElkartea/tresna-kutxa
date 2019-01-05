from django.contrib.postgres.fields import IntegerRangeField

from django_filters import FilterSet
from django_filters.filters import ChoiceFilter, NumericRangeFilter

from .fields import get_languages
from .models import Material, Activity, Reading, Video, Link, COMMON_LANGUAGES
from .widgets import RangeWidget


class MaterialFilterSet(FilterSet):
    class Meta:
        model = Material
        fields = ['subjects']


class IncludeNullMixin:
    def filter(self, qs, value):
        return super().filter(qs, value) | self.get_method(qs)(**{self.field_name: None})


class IncludeNullNumericRangeFilter(IncludeNullMixin, NumericRangeFilter):
    pass


class ActivityFilterSet(FilterSet):
    num_people = NumericRangeFilter(
            widget=RangeWidget(attrs={'min': 0, 'max': 40}),
            lookup_expr='overlap')

    duration = IncludeNullNumericRangeFilter(
            widget=RangeWidget(attrs={'min': 0, 'max': 360}),
            lookup_expr='range')

    class Meta:
        model = Activity
        fields = ['subjects', 'location', 'group_feature', 'num_people', 'duration']


class ReadingFilterSet(FilterSet):
    languages = ChoiceFilter(choices=get_languages(limit_to=COMMON_LANGUAGES))

    class Meta:
        model = Reading
        fields = ['subjects', 'pages', 'year', 'languages']


class VideoFilterSet(FilterSet):
    audios = ChoiceFilter(choices=get_languages(prioritize=COMMON_LANGUAGES))
    subtitles = ChoiceFilter(choices=get_languages(limit_to=COMMON_LANGUAGES))

    class Meta:
        model = Video
        fields = ['subjects', 'duration', 'year', 'audios', 'subtitles']


class LinkFilterSet(FilterSet):
    class Meta:
        model = Link
        fields = ['subjects']
