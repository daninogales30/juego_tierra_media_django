import random
from email.errors import CloseBoundaryNotFoundDefect

from django.db import models

from character.models import Character


class Battle(models.Model):
    character1 = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character1' )
    character2 = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character2' )
    winner = models.ForeignKey(Character,null=True, blank=True, on_delete=models.SET_NULL, related_name='ganador_batalla' )
    date = models.DateTimeField(auto_now_add=True)
    loser = models.ForeignKey(Character, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name='perdedor_batalla')

    def simulate(self):
        if not self.character1.arma_equipada or not self.character2.arma_equipada:
            raise ValueError("¡Ambos necesitan armas!")

        vida_max1 = self.character1.get_max_health()
        vida_max2 = self.character2.get_max_health()
        vida_actual1 = vida_max1
        vida_actual2 = vida_max2
        numero_ronda = 1


        stamina1 = 100
        stamina2 = 100
        critico = 0.10

        while vida_actual1 > 0 and vida_actual2 > 0:
            damage, _ = self.calculate_damage(self.character1, stamina1, critico)
            vida_actual2 = max(vida_actual2 - damage, 0)
            if vida_actual2 <= 0:
                break

            damage, _ = self.calculate_damage(self.character2, stamina2, critico)
            vida_actual1 = max(vida_actual1 - damage, 0)
            stamina2 = max(stamina2 - 15, 0)

            numero_ronda += 1
            if numero_ronda > 20:
                break

        if vida_actual1 > 0:
            winner = self.character1
            loser = self.character2
        elif vida_actual2 > 0:
            winner = self.character2
            loser = self.character1
        else:
            winner = random.choice([self.character1, self.character2])
            loser = self.character2 if winner == self.character1 else self.character1

        self.winner = winner
        self.loser = loser
        winner.health = max(int(0.3 * winner.get_max_health()), 1)
        loser.health = 0
        winner.save()
        loser.save()
        self.save()

    def calculate_damage(self, attacker, stamina, base_crit):
        base_damage = attacker.arma_equipada.potencia
        crit_multiplier = 2.5

        crit_chance = base_crit + ((100 - stamina) / 100 * 0.15)

        is_critical = random.random() < crit_chance

        damage = base_damage * (0.8 + random.random() * 0.4)
        if is_critical:
            damage *= crit_multiplier

        return int(damage), is_critical


    def __str__(self):
        return f"Batalla: {self.character1} vs {self.character2}"