from django_filters import FilterSet

import django_filters
from django_filters.filters import ChoiceFilter

from .fields import get_languages
from .models import Activity, Reading, Video, Link, COMMON_LANGUAGES


class ActivityFilter(FilterSet):
    class Meta:
        model = Activity
        fields = ['subjects', 'location', 'duration', 'min_people',
                'max_people', 'group_feature']


class ReadingFilter(FilterSet):
    languages = ChoiceFilter(choices=get_languages(limit_to=COMMON_LANGUAGES))

    class Meta:
        model = Reading
        fields = ['subjects', 'pages', 'year', 'languages']


class VideoFilter(FilterSet):
    audios = ChoiceFilter(choices=get_languages(prioritize=COMMON_LANGUAGES))
    subtitles = ChoiceFilter(choices=get_languages(limit_to=COMMON_LANGUAGES))

    class Meta:
        model = Video
        fields = ['subjects', 'duration', 'year', 'audios', 'subtitles']


class LinkFilter(FilterSet):
    class Meta:
        model = Link
        fields = ['subjects']
