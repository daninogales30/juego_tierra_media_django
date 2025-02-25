from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Weapon, Armor


@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
   # Solo agregamos las armas precargadas si no existen ya
   if not Weapon.objects.exists():
       Weapon.objects.create(name='arco', tipo='weapon', potencia=40, alcance=10)
       Weapon.objects.create(name='ballesta', tipo='weapon', potencia=47, alcance=10)
       Weapon.objects.create(name='espada', tipo='weapon', potencia=45, alcance=4)
       Weapon.objects.create(name='hacha', tipo='weapon', potencia=34, alcance=2)
       Weapon.objects.create(name='lanza', tipo='weapon', potencia=20, alcance=7)
       Weapon.objects.create(name='mazo', tipo='weapon', potencia=25, alcance=3)
       Weapon.objects.create(name='palanca', tipo='weapon', potencia=15, alcance=1)
