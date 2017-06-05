from modeltranslation.translator import register, TranslationOptions

from .models import (Subject, Goal, GroupFeature, Location, Language,
                     Approval, Material, Activity, Reading, Video, Link)


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


@register(Material)
class MaterialTranslationOptions(TranslationOptions):
    fields = ['title', 'brief']


# These inherit the translated fields from Material.
# Still, they need to be registered so that the modeltranslation admin wrapper
# works.

@register(Activity)
class ActivityTranslationOptions(TranslationOptions):
    fields = ['notes']


@register(Reading)
class ReadingTranslationOptions(TranslationOptions):
    fields = []


@register(Video)
class ReadingTranslationOptions(TranslationOptions):
    fields = []


@register(Link)
class LinkTranslationOptions(TranslationOptions):
    fields = []
