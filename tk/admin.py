from collections import OrderedDict

from django.contrib.auth.models import User, Group
from django.apps import apps
from django.contrib.admin import AdminSite
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from tk.material import admin as ma
from tk.material import models as mo

class TKAdmin(AdminSite):
    site_header = _("TK admin")
    site_title = _("TK admin")
    index_template = 'admin/tk_index.html'
    grouping = OrderedDict([
            (_("Material"), [
                'material.Activity',
                'material.Video',
                'material.Reading',
                'material.Link',
            ]),
            (_("Material classification"), [
                'material.Subject',
                'material.GroupFeature',
                'material.Location',
            ]),
            (_("Auth"), [
                'auth.User',
                'auth.Group',
            ]),
    ])

    def get_app_list(self, request):
        # Build the original app list so that we take into account user perms
        app_list = super().get_app_list(request)
        for g in self.grouping:
            yield {'name': g,
                   'models': [ self._get_model(m, app_list) for m in
                               self.grouping[g] ]}

    def _get_model(self, model, app_list):
        app_name, model_name = model.split('.')
        for a in app_list:
            if a['app_label'] == app_name:
                for m in a['models']:
                    if m['object_name'] == model_name:
                        return m

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        # Add notifications about pending approval requests
        Approval = apps.get_model('material', 'Approval')
        extra_context['approvals_new'] = Approval.objects.filter(
                timestamp__gte=request.user.last_login, approved=False)
        extra_context['approvals_unapproved'] = Approval.objects.filter(
                approved=False)

        return super().index(request, extra_context)

    def app_index(self, request, app_label, extra_context=None):
        # Disallow app indices: redirect to main index
        index_path = reverse('admin:index', current_app=self.name)
        return HttpResponseRedirect(index_path)


tkadmin = TKAdmin()
tkadmin.register(mo.Subject, ma.LocalizedAdmin)
tkadmin.register(mo.GroupFeature, ma.LocalizedAdmin)
tkadmin.register(mo.Location, ma.LocalizedAdmin)
tkadmin.register(mo.Approval, ma.ApprovalAdmin)
tkadmin.register(mo.Activity, ma.ActivityAdmin)
tkadmin.register(mo.Reading, ma.ReadingAdmin)
tkadmin.register(mo.Video, ma.VideoAdmin)
tkadmin.register(mo.Link, ma.LinkAdmin)
tkadmin.register(User)
tkadmin.register(Group)
