from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import AdminSite

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
            (_("Approval requests"), [
                'material.Approval',
            ]),
            (_("Material classification"), [
                'material.Subject',
                'material.Goal',
                'material.GroupFeature',
                'material.Location',
            ]),
            # TODO: Users and groups
    ])

    def get_app_list(self, request):
        # Build the original app list so that we take into account user perms
        app_list = super().get_app_list(request)
        return self.group_models(app_list)

    def group_models(self, app_list):
        for g in self.grouping:
            group = {'name': g, 'models': []}
            for m in self.grouping[g]:
                group['models'].append(self._get_model(m, app_list))
            yield group

    def _get_model(self, model, app_list):
        app_name, model_name = model.split('.')
        for a in app_list:
            if a['app_label'] == app_name:
                for m in a['models']:
                    if m['object_name'] == model_name:
                        return m


tkadmin = TKAdmin()
tkadmin.register(mo.Subject, ma.TranslationAdmin)
tkadmin.register(mo.Goal, ma.TranslationAdmin)
tkadmin.register(mo.GroupFeature, ma.TranslationAdmin)
tkadmin.register(mo.Location, ma.TranslationAdmin)
tkadmin.register(mo.Approval, ma.ApprovalAdmin)
tkadmin.register(mo.Activity, ma.ActivityAdmin)
tkadmin.register(mo.Reading, ma.ReadingAdmin)
tkadmin.register(mo.Video, ma.VideoAdmin)
tkadmin.register(mo.Link, ma.LinkAdmin)

# TODO: Users and groups
