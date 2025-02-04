from django.contrib import admin

from equipment.models import Weapon, Armor, Equipment

admin.site.register(Equipment)
admin.site.register(Weapon)
admin.site.register(Armor)
