from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Weapon, Armor


@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
   # Solo agregamos las armas precargadas si no existen ya
   if not Weapon.objects.exists():
       Weapon.objects.create(name='Espada de Fuego', tipo='weapon', potencia=10, alcance=5)
       Weapon.objects.create(name='Arco de las Sombras', tipo='weapon', potencia=7, alcance=10)
       Weapon.objects.create(name='Daga Venenosa', tipo='weapon', potencia=5, alcance=3)
