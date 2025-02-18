from django import forms
from character.models import Character

class BattleForm(forms.Form):
    jugador1 = forms.ModelChoiceField(queryset=Character.objects.all(), label="Jugador1")
    jugador2 = forms.ModelChoiceField(queryset=Character.objects.all(), label="Jugador2")
