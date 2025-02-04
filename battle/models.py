import random
from django.db import models
from character.models import Character

class Battle(models.Model):
    character1 = models.ForeignKey(Character, on_delete=models.CASCADE)
    character2 = models.ForeignKey(Character, on_delete=models.CASCADE)
    winner = models.ForeignKey(Character,null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def simulate(self):
        if not self.character1.arma_equipada or not self.character2.arma_equipada:
            raise ValueError("Ambos tienen que tener un arma equipada para pelear")

        potencia_arma1 = self.character1.get_power()
        potencia_arma2 = self.character2.get_power()

        probabilidad1 = potencia_arma1 / (potencia_arma2 + potencia_arma1)

        resultado = random.random()

        self.winner = self.character1 if resultado < probabilidad1 else self.character2
        self.save()

    def __str__(self):
        return f"Batalla entre {self.character1.name} y {self.character2.name}, y el ganador es... {self.winner if self.winner else 'Pendiente'}"
