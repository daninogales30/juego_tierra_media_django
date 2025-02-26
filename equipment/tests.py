from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from character.models import Character
from equipment.models import Equipment, Weapon


class EquipmentModelTest(TestCase):

    def test_equipment_creation(self):
        equipment = Equipment.objects.create(
            name="Espada",
            tipo="weapon",
            potencia=10
        )
        self.assertEqual(equipment.name, "Espada")
        self.assertEqual(equipment.tipo, "weapon")
        self.assertEqual(equipment.potencia, 10)
        self.assertTrue(equipment.es_arma())

    def test_equipment_str_method(self):
        equipment = Equipment.objects.create(
            name="Escudo",
            tipo="armor",
            potencia=5
        )
        self.assertEqual(str(equipment), "Escudo")

class WeaponModelTest(TestCase):

    def test_weapon_creation(self):
        weapon = Weapon.objects.create(
            name="Arco",
            tipo="weapon",
            potencia=8,
            alcance=100
        )

        self.assertEqual(weapon.name, "Arco")
        self.assertEqual(weapon.tipo, "weapon")
        self.assertEqual(weapon.potencia, 8)
        self.assertEqual(weapon.alcance, 100)
        self.assertTrue(weapon.es_arma())
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
