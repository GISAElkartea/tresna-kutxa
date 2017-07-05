from django.core.urlresolvers import reverse
from django.http import HttpResponseNotAllowed
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .models import Material, Activity, Video, Reading, Link
from .forms import ApprovalEmailForm, ActivityForm, VideoForm, ReadingForm, LinkForm


class CreateMaterial(FormView):
    template_name = 'material/create_material.html'

    FORM_CLASSES = {
        'approval': ApprovalEmailForm,
        'activity': ActivityForm,
        'video': VideoForm,
        'reading': ReadingForm,
        'link': LinkForm,
    }

    def get(self, *args, **kwargs):
        if self.kwargs.get('type') is None:
            return super().get(*args, **kwargs)
        return HttpResponseNotAllowed(['POST'])

    def get_form_name(self, mat_type):
        return '{}_form'.format(mat_type)

    def post(self, *args, **kwargs):
        if self.kwargs['type'] not in self.FORM_CLASSES.keys():
            return HttpResponseNotAllowed(['GET'])

        forms = self.get_named_forms()
        approval_form = forms[self.get_form_name('approval')]
        if approval_form.is_valid():
            approval = approval_form.save(commit=False)
        else:
            approval = Approval()
        material_form_name = self.get_form_name(self.kwargs['type'])

        if forms[material_form_name].is_valid():
            return self.form_valid(forms[material_form_name], approval)
        else:
            return self.form_invalid(**{
                material_form_name: forms[material_form_name]})

    def get_named_forms(self):
        forms = {}
        for mat_type, form_class in self.FORM_CLASSES.items():
            form_kwargs = self.get_form_kwargs()
            form_kwargs['prefix'] = mat_type
            forms[self.get_form_name(mat_type)] = form_class(**form_kwargs)
        return forms

    def form_valid(self, form, approval):
        self.object = form.save()
        approval.material = self.object.material_ptr
        approval.save()
        return super().form_valid(form)

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        # Shortcircuit FormMixin logic
        kwargs['form'] = None
        ctxt = self.get_named_forms()
        ctxt.update(kwargs)
        return super().get_context_data(**ctxt)

    def get_success_url(self):
        return reverse('frontpage')


class ListMaterial(ListView):
    queryset = Material.objects.approved()


class DetailActivity(DetailView):
    queryset = Activity.objects.approved()


class DetailVideo(DetailView):
    queryset = Video.objects.approved()


class DetailReading(DetailView):
    queryset = Reading.objects.approved()


class DetailLink(DetailView):
    queryset = Link.objects.approved()
