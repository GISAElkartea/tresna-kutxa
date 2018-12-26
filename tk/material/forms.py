from django.forms import ModelForm, EmailField

from captcha.fields import CaptchaField

from .models import Approval, Activity, Video, Reading, Link
from .widgets import LocalizedMarkdownxWidget


class MaterialForm(ModelForm):
    captcha = CaptchaField()
    email = EmailField()

    class Meta:
        widgets = {'goal': LocalizedMarkdownxWidget,
                   'brief': LocalizedMarkdownxWidget,}

    def save(self, commit=True, *args, **kwargs):
        super().save()
        Approval(email=self.cleaned_data['email'], material=self.instance).save()
        return self.instance
        

class ActivityForm(MaterialForm):
    class Meta(MaterialForm.Meta):
        model = Activity
        fields = '__all__'


class VideoForm(MaterialForm):
    class Meta(MaterialForm.Meta):
        model = Video
        fields = '__all__'


class ReadingForm(MaterialForm):
    class Meta(MaterialForm.Meta):
        model = Reading
        fields = '__all__'


class LinkForm(MaterialForm):
    class Meta(MaterialForm.Meta):
        model = Link
        fields = '__all__'
