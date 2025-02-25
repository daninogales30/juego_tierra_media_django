from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from character.models import Character, Relacion


class CharacterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.character = Character.objects.create(name='Hero', owner=self.user)

    def test_create_character_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('character:create_character'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'character_form.html')

    def test_character_list_view(self):
        response = self.client.get(reverse('character:character_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hero')

    def test_delete_character_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('character:delete_character', args=[self.character.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Character.objects.filter(id=self.character.id).exists())


class EquipWeaponTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.character = Character.objects.create(name='Hero', owner=self.user)

    def test_equip_weapon(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('character:equip_weapon', args=[self.character.id]),
                                    {'arma_equipada': 'Espada'})
        self.character.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.character.arma_equipada, 'Espada')


class RelacionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.character1 = Character.objects.create(name='Hero', owner=self.user)
        self.character2 = Character.objects.create(name='Villain', owner=self.user)

    def test_create_relacion(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('character:create_relacion'), {
            'character1': self.character1.id,
            'character2': self.character2.id,
            'relation_type': 'enemigo'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Relacion.objects.filter(character1=self.character1, character2=self.character2).exists())
