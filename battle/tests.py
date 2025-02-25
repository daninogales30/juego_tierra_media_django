from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from battle.models import Battle
from character.models import Character
from equipment.models import Weapon


class BattleViewTest(TestCase):
    def setUp(self):
        self.weapon = Weapon.objects.create(name="Espada", damage=10)
        self.character1 = Character.objects.create(name="Guerrero", health=100)
        self.character2 = Character.objects.create(name="Mago", health=100)
        self.character1.arma_equipada = self.weapon
        self.character2.arma_equipada = self.weapon
        self.character1.save()
        self.character2.save()

    def test_battle_view_loads(self):
        response = self.client.get(reverse("battle:battle_view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "battleview.html")

    def test_cannot_fight_self(self):
        response = self.client.post(reverse("battle:battle_view"), {
            "jugador1": self.character1.id,
            "jugador2": self.character1.id
        })
        self.assertFormError(response, "form", "jugador1", "No se puede pelear con el mismo personaje")

    def test_cannot_fight_without_weapon(self):
        self.character2.arma_equipada = None
        self.character2.save()

        response = self.client.post(reverse("battle:battle_view"), {
            "jugador1": self.character1.id,
            "jugador2": self.character2.id
        })
        self.assertFormError(response, "form", "jugador1", "Se necesita equipar un arma en ambos personajes")

    def test_successful_battle(self):
        response = self.client.post(reverse("battle:battle_view"), {
            "jugador1": self.character1.id,
            "jugador2": self.character2.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("ganador", response.context)
        self.assertTrue(Battle.objects.exists())
