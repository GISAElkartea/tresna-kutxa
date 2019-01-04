from django.contrib.postgres.fields import IntegerRangeField
from django_filters import FilterSet
from django_filters.filters import ChoiceFilter, NumericRangeFilter

from .fields import get_languages
from .models import Material, Activity, Reading, Video, Link, COMMON_LANGUAGES


class MaterialFilterSet(FilterSet):
    class Meta:
        model = Material
        fields = ['subjects']


class ActivityFilterSet(FilterSet):
    class Meta:
        model = Activity
        fields = {
                'subjects': ['exact'],
                'location': ['exact'],
                'duration': ['exact'],
                'num_people': ['contains'],
                'group_feature': ['exact'],
                }
        filter_overrides = {
            IntegerRangeField: {'filter_class': NumericRangeFilter}
        }



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
