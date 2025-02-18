from django import forms
from equipment.models import Equipment
from character.models import Character

class AssignEquipmentForm(forms.Form):
    character = forms.ModelChoiceField(queryset=Character.objects.all(), label="Selecciona un personaje")
    equipment = forms.ModelChoiceField(queryset=Equipment.objects.all(), label="Selecciona un equipo")
