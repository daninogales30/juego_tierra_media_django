from django import forms
from character.models import Character

class BattleForm(forms.Form):
    character1 = forms.ModelChoiceField(queryset=Character.objects.all(), label='Personaje 1')
    character2 = forms.ModelChoiceField(queryset=Character.objects.all(), label='Personaje 2')
