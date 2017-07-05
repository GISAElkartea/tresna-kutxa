from django.forms import ModelForm

from captcha.fields import CaptchaField

from .models import Approval, Activity, Video, Reading, Link


class ApprovalEmailForm(ModelForm):
    class Meta:
        model = Approval
        fields = ['email']


class ActivityForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Activity
        localized_fields = ['duration']  # TODO: Check
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].required = False


class VideoForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Video
        localized_fields = ['duration']  # TODO: Check
        fields = '__all__'


class ReadingForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Reading
        fields = '__all__'


class LinkForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Link
        fields = '__all__'
