from django.forms import ModelForm

from .models import Approval, Activity, Video, Reading, Link

# TODO: Captcha


class ApprovalEmailForm(ModelForm):
    class Meta:
        model = Approval
        fields = ['email']


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        localized_fields = ['duration']  # TODO: Check
        fields = '__all__'


class VideoForm(ModelForm):
    class Meta:
        model = Video
        localized_fields = ['duration']  # TODO: Check
        fields = '__all__'


class ReadingForm(ModelForm):
    class Meta:
        model = Reading
        fields = '__all__'


class LinkForm(ModelForm):
    class Meta:
        model = Link
        fields = '__all__'
