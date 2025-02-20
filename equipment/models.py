from django.db import models

# Create your models here.
class Equipment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=50, choices=[('weapon', 'Weapon'), ('armor', 'Armor')])
    potencia = models.IntegerField()
    imagen = models.ImageField(upload_to='equipment/', null=True, blank=True)

    def es_arma(self):
        return self.tipo.lower() == 'weapon'

    def __str__(self):
        return f"{self.name}"


class Weapon(Equipment):
    alcance = models.IntegerField()

class Armor(Equipment):
    endurance = models.IntegerField()