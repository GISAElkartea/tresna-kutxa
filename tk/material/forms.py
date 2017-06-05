from django.forms import ModelForm

from modeltranslation.translator import translator, NotRegistered

from .models import Approval, Activity, Video, Reading, Link

# TODO: Captcha

class TranslatedModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            opts = translator.get_options_for_model(self._meta.model)
        except NotRegistered:
            return
        for field in opts.get_field_names():
            del self.fields[field]


class ApprovalEmailForm(TranslatedModelForm):
    class Meta:
        model = Approval
        fields = ['email']


class ActivityForm(TranslatedModelForm):
    class Meta:
        model = Activity
        localized_fields = ['duration']  # TODO: Check
        fields = '__all__'


class VideoForm(TranslatedModelForm):
    class Meta:
        model = Video
        localized_fields = ['duration']  # TODO: Check
        fields = '__all__'


class ReadingForm(TranslatedModelForm):
    class Meta:
        model = Reading
        fields = '__all__'


class LinkForm(TranslatedModelForm):
    class Meta:
        model = Link
        fields = '__all__'
