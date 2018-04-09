from django.urls import reverse
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from watson import search as watson

from .models import Approval, Material, Activity, Video, Reading, Link
from .forms import ApprovalEmailForm, ActivityForm, VideoForm, ReadingForm, LinkForm


class SubtypeFormMixin(object):

    named_subtypes = {}

    def get_named_subtypes(self):
        return self.named_subtypes

    def get_subtype_instance(self, name):
        return self.get_named_subtypes()[name]()

    def get_named_subtype_instances(self):
        return {name: self.get_subtype_instance(name)
                for name in self.get_named_subtypes()}

    def get_context_data(self, **kwargs):
        ctxt = self.get_named_subtype_instances()
        ctxt.update(kwargs)
        return super().get_context_data(**ctxt)

    def get_subtype(self, *args, **kwargs):
        return self.kwargs.get('type', '')

    def get(self, *args, **kwargs):
        if self.get_subtype(*args, **kwargs):
            return HttpResponseNotAllowed(['POST'])
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        subtype = self.get_subtype(*args, **kwargs)
        if subtype not in self.get_named_subtypes():
            return HttpResponseNotAllowed(['GET'])
        return self.subtype_post(subtype, *args, **kwargs)


class CreateMaterial(SubtypeFormMixin, FormView):
    template_name = 'material/create_material.html'
    named_subtypes = {
        'approval_form': ApprovalEmailForm,
        'activity_form': ActivityForm,
        'video_form': VideoForm,
        'reading_form': ReadingForm,
        'link_form': LinkForm,
    }

    def get_subtype(self, *args, **kwargs):
        t = self.kwargs.get('type', '')
        return '{}_form'.format(t) if t else None

    def get_subtype_instance(self, name):
        kwargs = self.get_form_kwargs()
        kwargs['prefix'] = name
        return self.get_named_subtypes()[name](**kwargs)

    def subtype_post(self, subtype, *args, **kwargs):
        forms = self.get_named_subtype_instances()

        approval = Approval()
        if forms['approval_form'].is_valid():
            approval = forms['approval_form'].save(commit=False)

        if forms[subtype].is_valid():
            return self.form_valid(subtype, forms[subtype], approval)
        return self.form_invalid(subtype, forms[subtype], approval)

    def form_valid(self, subtype, form, approval):
        self.object = form.save()
        approval.material = self.object.material_ptr
        approval.save()
        return super().form_valid(form)

    def form_invalid(self, subtype, form, approval):
        ctxt = {subtype: form}
        return self.render_to_response(self.get_context_data(**ctxt))

    def get_context_data(self, **kwargs):
        # Shortcircuit FormMixin logic
        kwargs['form'] = None
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()


class LocalizedSlugMixin(SingleObjectMixin):
    def get_slug_field(self):
        slug_field = super().get_slug_field()
        lang_code = getattr(self.request, 'LANGUAGE_CODE', None)
        if lang_code is not None:
            return '{}__{}'.format(slug_field, lang_code)
        return slug_field


class PendingApprovalMixin():
    def get_template_names(self):
        if hasattr(self.object, 'approval') and not self.object.approval.approved:
            return ['material/pending.html']
        return super().get_template_names()


class DetailActivity(LocalizedSlugMixin, PendingApprovalMixin, DetailView):
    model = Activity


class DetailVideo(LocalizedSlugMixin, PendingApprovalMixin, DetailView):
    model = Video


class DetailReading(LocalizedSlugMixin, PendingApprovalMixin, DetailView):
    model = Reading


class DetailLink(LocalizedSlugMixin, PendingApprovalMixin, DetailView):
    model = Link


class SearchMaterial(ListView):
    template_name = 'material/material_search.html'
    query_param = 'q'

    def get_query(self):
        return self.request.GET.get(self.query_param, '').strip()

    def get_queryset(self):
        return watson.filter(Material.objects.approved(), self.get_query())
