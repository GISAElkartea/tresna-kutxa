from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from .models import Activity, Video, Reading, Link
from .forms import ApprovalEmailForm, ActivityForm, VideoForm, ReadingForm, LinkForm


class ApprovalMixin():
    def get_context_data(self, **kwargs):
        kwargs['approval_form'] = ApprovalEmailForm()
        return super().get_context_data(**kwargs)

    def get_approval(self):
        approval_form = ApprovalEmailForm(data=self.request.POST)
        if approval_form.is_valid():
            return approval_form.save(commit=False)
        return Approval()


class MaterialCreationMixin(ApprovalMixin):
    def form_valid(self, form):
        # Sets self.object
        response = super().form_valid(form)
        approval = self.get_approval()
        setattr(approval, self.object.APPROVAL_RESOURCE_KEY, self.object)
        approval.save()
        return response


class CreateActivity(MaterialCreationMixin, CreateView):
    template_name = 'material/submission/create_activity.html'
    form_class = ActivityForm


class CreateVideo(MaterialCreationMixin, CreateView):
    template_name = 'material/submission/create_video.html'
    form_class = VideoForm


class CreateReading(MaterialCreationMixin, CreateView):
    template_name = 'material/submission/create_reading.html'
    form_class = ReadingForm


class CreateLink(MaterialCreationMixin, CreateView):
    template_name = 'material/submission/create_link.html'
    form_class = LinkForm


class DetailActivity(DetailView):
    queryset = Activity.objects.approved()


class DetailVideo(DetailView):
    queryset = Video.objects.approved()


class DetailReading(DetailView):
    queryset = Reading.objects.approved()


class DetailLink(DetailView):
    queryset = Link.objects.approved()
