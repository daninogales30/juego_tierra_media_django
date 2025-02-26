import random
from django.db import models

from character.models import Character


class Battle(models.Model):
    character1 = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character1' )
    character2 = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character2' )
    winner = models.ForeignKey(Character,null=True, blank=True, on_delete=models.SET_NULL, related_name='ganador_batalla' )
    date = models.DateTimeField(auto_now_add=True)
    battle_log = models.TextField(blank=True)  # Nuevo campo para registrar la batalla

    def simulate(self):
        self.battle_log = ""  # Resetear log
        if not self.character1.arma_equipada or not self.character2.arma_equipada:
            raise ValueError("¡Ambos necesitan armas!")

        # Configurar atributos iniciales
        max_health1 = self.character1.get_max_health()
        max_health2 = self.character2.get_max_health()
        current_health1 = max_health1
        current_health2 = max_health2
        round_number = 1

        # Nuevos atributos de combate
        stamina1 = 100
        stamina2 = 100
        critical_chance = 0.15  # 15% base de golpe crítico

        while current_health1 > 0 and current_health2 > 0:
            self.battle_log += f"\n⚔️ RONDA {round_number}:\n"

            # Personaje 1 ataca
            damage, is_critical = self.calculate_damage(self.character1, stamina1, critical_chance)
            current_health2 = max(current_health2 - damage, 0)
            stamina1 = max(stamina1 - 15, 0)
            self.log_attack(self.character1, self.character2, damage, is_critical)

            if current_health2 <= 0:
                break

            # Personaje 2 ataca
            damage, is_critical = self.calculate_damage(self.character2, stamina2, critical_chance)
            current_health1 = max(current_health1 - damage, 0)
            stamina2 = max(stamina2 - 15, 0)
            self.log_attack(self.character2, self.character1, damage, is_critical)

            round_number += 1
            if round_number > 20:  # Evitar bucles infinitos
                break

        # Determinar ganador
        if current_health1 > 0:
            winner = self.character1
            loser = self.character2
        else:
            winner = self.character2
            loser = self.character1

        # Actualizar salud y stamina
        winner.health = int(0.3 * winner.get_max_health())
        loser.health = 0
        winner.save()
        loser.save()

        self.winner = winner
        self.save()

    def calculate_damage(self, attacker, stamina, base_crit):
        base_damage = attacker.arma_equipada.potencia
        crit_multiplier = 2.5  # Multiplicador de daño crítico

        # Aumentar probabilidad crítica si stamina es baja
        crit_chance = base_crit + ((100 - stamina) / 100 * 0.15)
        is_critical = random.random() < crit_chance

        # Calcular daño con variación
        damage = base_damage * (0.8 + random.random() * 0.4)  # Variación 80-120%
        if is_critical:
            damage *= crit_multiplier

        return int(damage), is_critical

    def log_attack(self, attacker, defender, damage, is_critical):
        crit_msg = " ¡CRÍTICO! 💥" if is_critical else ""
        messages = [
            f"{attacker.name} golpea a {defender.name} con {attacker.arma_equipada.name} (-{damage} HP){crit_msg}",
            f"¡{attacker.name} realiza un combo espectacular! 🔥",
            f"¡Esquivo magistral de {defender.name}! 🌀",
            f"¡Ataque fulminante de {attacker.name}! ⚡"
        ]
        self.battle_log += random.choice(messages) + "\n"

    def __str__(self):
        return f"Batalla: {self.character1} vs {self.character2}"