from django.forms import ModelForm

from captcha.fields import CaptchaField

from .models import Approval, Activity, Video, Reading, Link
from .widgets import LocalizedMarkdownxWidget


class ApprovalEmailForm(ModelForm):
    class Meta:
        model = Approval
        fields = ['email']


material_widgets = {
        'goal': LocalizedMarkdownxWidget,
        'brief': LocalizedMarkdownxWidget,
        }

class ActivityForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Activity
        localized_fields = ['duration']  # TODO: Check
        fields = '__all__'
        widgets = material_widgets

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].required = False


class VideoForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Video
        localized_fields = ['duration']  # TODO: Check
        fields = '__all__'
        widgets = material_widgets


class ReadingForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Reading
        fields = '__all__'
        widgets = material_widgets


class LinkForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Link
        fields = '__all__'
        widgets = material_widgets
