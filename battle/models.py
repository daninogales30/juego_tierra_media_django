import random
from django.db import models
from django.utils import timezone
from character.models import Character


class Battle(models.Model):
    ATTACK_TYPES = (
        ('MELEE', 'Ataque cuerpo a cuerpo'),
        ('RANGED', 'Ataque a distancia'),
        ('MAGIC', 'Ataque mágico'),
    )

    character1 = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='attacker')
    character2 = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='defender')
    winner = models.ForeignKey(Character, null=True, blank=True, on_delete=models.SET_NULL)
    rounds = models.PositiveIntegerField(default=0)
    attack_log = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    battle_history = models.JSONField(default=list)  # Para almacenar el historial detallado

    def calculate_damage(self, attacker, defender, attack_type):
        base_damage = attacker.get_power()
        critical = random.random() < (attacker.agility / 1000)
        evasion = random.random() < (defender.agility / 1500)

        if evasion:
            return 0, 'evasion', attack_type

        if critical:
            base_damage *= 2

        # Modificadores por tipo de ataque
        modifiers = {
            'MELEE': attacker.strength * 0.1,
            'RANGED': attacker.agility * 0.1,
            'MAGIC': attacker.intelligence * 0.1
        }

        damage = base_damage + modifiers.get(attack_type, 0)
        damage_type = 'critical' if critical else 'normal'

        return int(damage), damage_type, attack_type

    def simulate_battle(self):
        self.battle_history = []
        fighters = [self.character1, self.character2]
        current_attacker, current_defender = random.sample(fighters, 2)

        while self.character1.health > 0 and self.character2.health > 0:
            self.rounds += 1
            attack_type = random.choice(['MELEE', 'RANGED', 'MAGIC'])

            damage, result, attack_type = self.calculate_damage(
                current_attacker,
                current_defender,
                attack_type
            )

            log_entry = {
                'attacker': current_attacker.name,
                'defender': current_defender.name,
                'damage': damage,
                'type': attack_type.lower(),
                'result': result,
                'attacker_health': current_attacker.health,
                'defender_health': current_defender.health
            }

            if result != 'evasion':
                current_defender.health = max(current_defender.health - damage, 0)
                current_defender.save()

            self.battle_history.append(log_entry)
            current_attacker, current_defender = current_defender, current_attacker

            if self.rounds >= 20:  # Límite de rondas
                break

        self.winner = self.character1 if self.character1.health > self.character2.health else self.character2
        self.save()