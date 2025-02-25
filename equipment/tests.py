from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from character.models import Character
from equipment.models import Equipment

class EquipmentViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        cls.character = Character.objects.create(name='Test Character')
        cls.equipment = Equipment.objects.create(name='Sword')

    def test_equipment_list_view(self):
        response = self.client.get(reverse('equipment:equipment_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipment_list.html')
        self.assertContains(response, self.equipment.name)

    def test_assign_equipment_view_get(self):
        response = self.client.get(reverse('equipment:assign_equipment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assign_equipment.html')

    def test_assign_equipment_view_post(self):
        response = self.client.post(reverse('equipment:assign_equipment'), {
            'character': self.character.id,
            'equipment': self.equipment.id
        })
        self.assertEqual(response.status_code, 302)
        self.character.refresh_from_db()
        self.assertIn(self.equipment, self.character.equipment.all())
