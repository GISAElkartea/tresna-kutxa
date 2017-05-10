from datetime import timedelta
from django.test import TestCase

from .models import Approval, ApprovalResource, Activity

class ApprovalQuerySetTestCase(TestCase):
    def setUp(self):
        self.material = Activity.objects.create(
                title="test",
                duration=timedelta(seconds=30),
                )

    def test_without_request_is_approved(self):
        self.assertTrue(Activity.objects.approved().exists())

    def test_accepted_material_is_approved(self):
        Approval.objects.create(
                resource=ApprovalResource.objects.create(activity=self.material),
                approved=True)
        self.assertTrue(Activity.objects.approved().exists())

    def test_rejected_material_is_not_approved(self):
        Approval.objects.create(
                resource=ApprovalResource.objects.create(activity=self.material),
                approved=False)
        self.assertFalse(Activity.objects.approved().exists())

    def test_without_is_not_unapproved(self):
        self.assertFalse(Activity.objects.unapproved().exists())

    def test_accepted_material_is_not_unnaproved(self):
        Approval.objects.create(
                resource=ApprovalResource.objects.create(activity=self.material),
                approved=True)
        self.assertFalse(Activity.objects.unapproved().exists())

    def test_rejected_material_is_unapproved(self):
        Approval.objects.create(
                resource=ApprovalResource.objects.create(activity=self.material),
                approved=False)
        self.assertTrue(Activity.objects.unapproved().exists())
