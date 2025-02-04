from django.db import models
from equipment.models import Equipment, Weapon

class Character(models.Model):
    name = models.CharField(max_length=50, unique=True)
    race = models.CharField(max_length=50, choices=[('elfo', 'Elfo'), ('humana', 'Humana'), ('Enano', 'Enano'), ('Hobbit', 'Hobbit')])
    faction = models.CharField(max_length=100)
    ubication = models.CharField(max_length=100)
    equipment = models.ManyToManyField(Equipment, blank=True, related_name='equipamiento')
    arma_equipada = models.ForeignKey(Weapon, null=True, blank=True, on_delete=models.SET_NULL, related_name='arma_equipada')

    def add_equipment(self, new_equipment):
        self.equipment.add(new_equipment)

    def equip_weapon(self, weapon):
        if weapon in self.equipment.all() and weapon.es_arma():
            self.arma_equipada = weapon
            self.save()
        else:
            raise ValueError("El arma no es válida.")

    def change_ubication(self, new_ubication):
        self.ubication = new_ubication
        self.save()

    def get_power(self):
        return self.arma_equipada.potencia if self.arma_equipada else "No se puede obtener la potencia de este arma"

    def __str__(self):
        return f"{self.name}"

class Relacion(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='personaje1')
    related_to = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='personaje2')
    tipo = models.CharField(max_length=50, choices=[('amigo', 'Amigo'), ('enemigo', 'Enemigo'), ('neutral', 'Neutral')])
    confidence_level = models.IntegerField(default=0)

    def __str__(self):
        return f"Relación: {self.character} con {self.related_to} de tipo '{self.tipo}' y con nivel de confianza '{self.confidence_level}'"

