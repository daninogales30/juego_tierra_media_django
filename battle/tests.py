from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from battle.models import Battle
from character.models import Character
from equipment.models import Weapon


from django.test import TestCase
from django.utils import timezone
from character.models import Character
from .models import Battle

class BattleModelTest(TestCase):

    def setUp(self):

        self.character1 = Character.objects.create(
            name="Guerrero",
            arma_equipada="Espada",
            potencia_arma=10,
            health=100,
            max_health=100
        )
        self.character2 = Character.objects.create(
            name="Arquero",
            arma_equipada="Arco",
            potencia_arma=8,
            health=100,
            max_health=100
        )

    def test_battle_creation(self):

        battle = Battle.objects.create(
            character1=self.character1,
            character2=self.character2
        )

        self.assertEqual(battle.character1, self.character1)
        self.assertEqual(battle.character2, self.character2)
        self.assertIsNone(battle.winner)
        self.assertIsNone(battle.loser)
        self.assertIsNotNone(battle.date)

    def test_battle_str_method(self):

        battle = Battle.objects.create(
            character1=self.character1,
            character2=self.character2
        )
        expected_str = f"Batalla: {self.character1} vs {self.character2}"
        self.assertEqual(str(battle), expected_str)

    def test_simulate_method_with_weapons(self):

        battle = Battle.objects.create(
            character1=self.character1,
            character2=self.character2
        )

        battle.simulate()

        self.assertIsNotNone(battle.winner)
        self.assertIsNotNone(battle.loser)
        self.assertIn(battle.winner, [self.character1, self.character2])
        self.assertIn(battle.loser, [self.character1, self.character2])

        self.assertNotEqual(battle.winner, battle.loser)

        self.assertEqual(battle.winner.health, max(int(0.3 * battle.winner.get_max_health()), 1))
        self.assertEqual(battle.loser.health, 0)

    def test_simulate_method_max_rounds(self):

        weak_character1 = Character.objects.create(
            name="Guerrero Débil",
            arma_equipada="Espada Débil",
            potencia_arma=1,
            health=1000,
            max_health=1000
        )
        weak_character2 = Character.objects.create(
            name="Arquero Débil",
            arma_equipada="Arco Débil",
            potencia_arma=1,
            health=1000,
            max_health=1000
        )
        battle = Battle.objects.create(
            character1=weak_character1,
            character2=weak_character2
        )

        battle.simulate()

        self.assertIsNotNone(battle.winner)
        self.assertIsNotNone(battle.loser)
        self.assertEqual(battle.winner.health, max(int(0.3 * battle.winner.get_max_health()), 1))
        self.assertEqual(battle.loser.health, 0)

    def test_simulate_method_without_weapons(self):

        character_without_weapon = Character.objects.create(
            name="Mago",
            arma_equipada=None,
            potencia_arma=0,
            health=100,
            max_health=100
        )
        battle = Battle.objects.create(
            character1=self.character1,
            character2=character_without_weapon
        )

        with self.assertRaises(ValueError):
            battle.simulate()


    def test_calculate_damage_method(self):

        battle = Battle.objects.create(
            character1=self.character1,
            character2=self.character2
        )
        damage, is_critical = battle.calculate_damage(self.character1, 100, 0.10)

        self.assertGreaterEqual(damage, int(self.character1.arma_equipada.potencia * 0.8))
        self.assertLessEqual(damage, int(self.character1.arma_equipada.potencia * 1.2 * 2.5))
        self.assertIsInstance(is_critical, bool)

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
        battle = Battle.objects.first()
        self.assertIsNotNone(battle.winner)
        self.assertIsNotNone(battle.loser)