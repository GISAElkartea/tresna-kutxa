from django.test import TestCase

from .models import Approval, Material

class ApprovalQuerySetTestCase(TestCase):
    def setUp(self):
        self.material = Material.objects.create(title="test")

    def test_without_request_is_approved(self):
        self.assertTrue(Material.objects.approved().exists())

    def test_accepted_material_is_approved(self):
        Approval.objects.create(material=self.material, approved=True)
        self.assertTrue(Material.objects.approved().exists())

    def test_rejected_material_is_not_approved(self):
        Approval.objects.create(material=self.material, approved=False)
        self.assertFalse(Material.objects.approved().exists())

    def test_without_is_not_unapproved(self):
        self.assertFalse(Material.objects.unapproved().exists())

    def test_accepted_material_is_not_unnaproved(self):
        Approval.objects.create(material=self.material, approved=True)
        self.assertFalse(Material.objects.unapproved().exists())

    def test_rejected_material_is_unapproved(self):
        Approval.objects.create(material=self.material, approved=False)
        self.assertTrue(Material.objects.unapproved().exists())
