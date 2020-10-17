from django.contrib.postgres.fields import IntegerRangeField
from django.db import models
from django import forms

from django_filters import FilterSet
from django_filters.filters import ModelMultipleChoiceFilter, MultipleChoiceFilter, NumericRangeFilter

from .fields import get_languages
from .models import Subject, Material, Activity, Reading, Video, Link, COMMON_LANGUAGES
from .widgets import RangeWidget, ToggleAllCheckboxSelectMultiple


class CommaSeparatedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def _check_values(self, value):
        if value:
            value = [v.rstrip().lstrip() for vs in value for v in vs.split(',')]
        return super()._check_values(value)

    def clean(self, value):
        if value:
            value = [v.rstrip().lstrip() for vs in value for v in vs.split(',')]
        return super().clean(value)



class SubjectFilter(ModelMultipleChoiceFilter):
    field_class = CommaSeparatedModelMultipleChoiceField

    def __init__(self, *args, **kwargs):
        if 'queryset' not in kwargs:
            kwargs['queryset'] = Subject.objects.all()
        if 'widget' not in kwargs:
            kwargs['widget'] = ToggleAllCheckboxSelectMultiple()
        kwargs['initial'] = lambda: kwargs['queryset'].values_list('pk', flat=True)
        super().__init__(*args, **kwargs)
        self.always_filter = False


class MaterialFilterSet(FilterSet):
    subjects = SubjectFilter()

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


class ActivityFilterSet(FilterSet):
    subjects = SubjectFilter()

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
    subjects = SubjectFilter()

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


class VideoFilterSet(FilterSet):
    subjects = SubjectFilter()

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


class LinkFilterSet(FilterSet):
    class Meta:
        model = Link
        fields = ['subjects']

    subjects = SubjectFilter()
