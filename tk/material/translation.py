from modeltranslation.translator import register, TranslationOptions

from .models import (Subject, Goal, GroupFeature, Location, Language,
                     Approval, Activity, Reading, Video, Link)


@register(Subject)
class SubjectTranslationOptions(TranslationOptions):
    fields = ['name']


@register(Goal)
class GoalTranslationOptions(TranslationOptions):
    fields = ['name']


@register(GroupFeature)
class GroupFeatureTranslationOptions(TranslationOptions):
    fields = ['name']


@register(Location)
class LocationTranslationOptions(TranslationOptions):
    fields = ['name']


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ['name']


@register(Activity)
class ActivityTranslationOptions(TranslationOptions):
    fields = ['title', 'brief', 'notes']


@register(Reading)
class ReadingTranslationOptions(TranslationOptions):
    fields = ['title', 'brief']


@register(Video)
class ReadingTranslationOptions(TranslationOptions):
    fields = ['title', 'brief']


@register(Link)
class LinkTranslationOptions(TranslationOptions):
    fields = ['title', 'brief']
