from django.forms import CheckboxSelectMultiple
from django.contrib.postgres.fields import IntegerRangeField
from django.db import models

from django_filters import FilterSet
from django_filters.filters import ModelMultipleChoiceFilter, MultipleChoiceFilter, NumericRangeFilter

from .fields import get_languages
from .models import Subject, Material, Activity, Reading, Video, Link, COMMON_LANGUAGES
from .widgets import RangeWidget


class MaterialFilterSet(FilterSet):
    class Meta:
        model = Material
        fields = ['subjects']

    subjects = ModelMultipleChoiceFilter(
            queryset=Subject.objects.all(),
            widget=CheckboxSelectMultiple())


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


class ActivityFilterSet(FilterSet):
    num_people = NumericRangeFilter(
            widget=RangeWidget(attrs={'min': 0, 'max': 40}),
            lookup_expr='overlap')

    duration = IncludeNullNumericRangeFilter(
            widget=RangeWidget(attrs={'min': 0, 'max': 360}),
            lookup_expr='range')

    subjects = ModelMultipleChoiceFilter(
            queryset=Subject.objects.all(),
            widget=CheckboxSelectMultiple())

    class Meta:
        model = Activity
        fields = ['subjects', 'location', 'group_feature', 'num_people', 'duration']


class ReadingFilterSet(FilterSet):
    languages = ArrayMultipleChoiceFilter(
            widget=CheckboxSelectMultiple(),
            choices=get_languages(limit_to=COMMON_LANGUAGES),
            lookup_expr='overlap')

    pages = IncludeNullNumericRangeFilter(
            widget=RangeWidget(attrs={'min': 0, 'max': 3000}),
            lookup_expr='range')

    subjects = ModelMultipleChoiceFilter(
            queryset=Subject.objects.all(),
            widget=CheckboxSelectMultiple())

    class Meta:
        model = Reading
        fields = ['subjects', 'pages', 'year', 'languages']


class VideoFilterSet(FilterSet):
    audios = ArrayMultipleChoiceFilter(
            widget=CheckboxSelectMultiple(),
            choices=get_languages(prioritize=COMMON_LANGUAGES),
            lookup_expr='overlap')

    subtitles = ArrayMultipleChoiceFilter(
            widget=CheckboxSelectMultiple(),
            choices=get_languages(limit_to=COMMON_LANGUAGES),
            lookup_expr='overlap')

    duration = IncludeNullNumericRangeFilter(
            widget=RangeWidget(attrs={'min': 0, 'max': 360}),
            lookup_expr='range')

    subjects = ModelMultipleChoiceFilter(
            queryset=Subject.objects.all(),
            widget=CheckboxSelectMultiple())

    class Meta:
        model = Video
        fields = ['subjects', 'duration', 'year', 'audios', 'subtitles']


class LinkFilterSet(FilterSet):
    class Meta:
        model = Link
        fields = ['subjects']

    subjects = ModelMultipleChoiceFilter(
            queryset=Subject.objects.all(),
            widget=CheckboxSelectMultiple())
