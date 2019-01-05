from django.forms import ModelForm, EmailField

from captcha.fields import CaptchaField

from .models import Approval, Activity, Video, Reading, Link
from .widgets import LocalizedMarkdownxWidget, RangeWidget


MATERIAL_WIDGETS = {'goal': LocalizedMarkdownxWidget,
                    'brief': LocalizedMarkdownxWidget,}

class MaterialForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    captcha = CaptchaField()
    email = EmailField()

    def save(self, commit=True, *args, **kwargs):
        super().save()
        Approval(email=self.cleaned_data['email'], material=self.instance).save()
        return self.instance
        

class ActivityForm(MaterialForm):
    class Meta:
        model = Activity
        fields = '__all__'
        widgets = dict(num_people=RangeWidget(), **MATERIAL_WIDGETS)


class VideoForm(MaterialForm):
    class Meta:
        model = Video
        fields = '__all__'
        widgets = MATERIAL_WIDGETS


class ReadingForm(MaterialForm):
    class Meta:
        model = Reading
        fields = '__all__'
        widgets = MATERIAL_WIDGETS


class LinkForm(MaterialForm):
    class Meta:
        model = Link
        fields = '__all__'
        widgets = MATERIAL_WIDGETS
