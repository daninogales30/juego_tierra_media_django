from django import forms
from character.models import Character, Relacion


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["name", "race", "faction", "ubication", "equipment", "arma_equipada"]

class RelacionForm(forms.ModelForm):
    class Meta:
        model = Relacion
        fields = ["character", "related_to", "tipo", "confidence_level"]