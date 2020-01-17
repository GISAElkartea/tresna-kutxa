from django.contrib.postgres.fields import IntegerRangeField
from django.db import models

from django_filters import FilterSet
from django_filters.filters import ModelMultipleChoiceFilter, MultipleChoiceFilter, NumericRangeFilter

from .fields import get_languages
from .models import Subject, Material, Activity, Reading, Video, Link, COMMON_LANGUAGES
from .widgets import RangeWidget, ToggleAllCheckboxSelectMultiple


class SubjectFilterSet(FilterSet):
    def __init__(self, data=None, *args, **kwargs):
        prefix = kwargs.get('prefix')
        field = 'subjects'
        if prefix:
            field = "{}-{}".format(prefix, field)
        if data is not None and field not in data:
            data = data.copy()
            data.setlist(field, Subject.objects.values_list('pk', flat=True))
        super(SubjectFilterSet, self).__init__(data, *args, **kwargs)

    subjects = ModelMultipleChoiceFilter(queryset=Subject.objects.all(),
                                         widget=ToggleAllCheckboxSelectMultiple())
    subjects.always_filter = False


class MaterialFilterSet(SubjectFilterSet):
    class Meta:
        model = Material
        fields = ['subjects']

class IncludeNullMixin:
    def filter(self, qs, value):
        return super().filter(qs, value) | self.get_method(qs)(**{self.field_name: None})


class IncludeNullNumericRangeFilter(IncludeNullMixin, NumericRangeFilter):
    pass


class ArrayChoiceMixin:
    def filter(self, qs, value):
        if not value:
            # Even though not a noop, no point filtering if empty.
            return qs
        if self.is_noop(qs, value):
            return qs
        lookup = '%s__%s' % (self.field_name, self.lookup_expr)
        qs = self.get_method(qs)(**{lookup: value})
        return qs.distinct() if self.distinct else qs


class ArrayMultipleChoiceFilter(ArrayChoiceMixin, MultipleChoiceFilter):
    pass


class ActivityFilterSet(SubjectFilterSet):
    num_people = NumericRangeFilter(
            widget=RangeWidget(attrs={'min': 0, 'max': 40}),
            lookup_expr='overlap')

    duration = IncludeNullNumericRangeFilter(
            widget=RangeWidget(attrs={'min': 0, 'max': 360}),
            lookup_expr='range')

    class Meta:
        model = Activity
        fields = ['subjects', 'location', 'group_feature', 'num_people', 'duration']


class ReadingFilterSet(SubjectFilterSet):
    languages = ArrayMultipleChoiceFilter(
            widget=ToggleAllCheckboxSelectMultiple(),
            choices=get_languages(limit_to=COMMON_LANGUAGES),
            lookup_expr='overlap')

    pages = IncludeNullNumericRangeFilter(
            widget=RangeWidget(attrs={'min': 0, 'max': 3000}),
            lookup_expr='range')

    class Meta:
        model = Reading
        fields = ['subjects', 'pages', 'year', 'languages']


class VideoFilterSet(SubjectFilterSet):
    audios = ArrayMultipleChoiceFilter(
            widget=ToggleAllCheckboxSelectMultiple(),
            choices=get_languages(prioritize=COMMON_LANGUAGES),
            lookup_expr='overlap')

    subtitles = ArrayMultipleChoiceFilter(
            widget=ToggleAllCheckboxSelectMultiple(),
            choices=get_languages(limit_to=COMMON_LANGUAGES),
            lookup_expr='overlap')

    duration = IncludeNullNumericRangeFilter(
            widget=RangeWidget(attrs={'min': 0, 'max': 360}),
            lookup_expr='range')

    class Meta:
        model = Video
        fields = ['subjects', 'duration', 'year', 'audios', 'subtitles']


class LinkFilterSet(SubjectFilterSet):
    class Meta:
        model = Link
        fields = ['subjects']
