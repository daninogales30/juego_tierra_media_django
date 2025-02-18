from django import forms
from character.models import Character, Relacion


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["name", "race", "faction", "ubication", "equipment", "arma_equipada"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Character.objects.filter(name=name).exists():
            raise forms.ValidationError("Ya existe un personaje con este nombre.")
        return name

class RelacionForm(forms.ModelForm):
    class Meta:
        model = Relacion
        fields = ["character", "related_to", "tipo", "confidence_level"]

    def clean(self):
        if self.cleaned_data.get("character") == self.cleaned_data.get("related_to"):
            raise forms.ValidationError("Un personaje no puede relacionarse consigo mismo.")
        return self.cleaned_data

    def save(self, commit=True):
        return Relacion.objects.update_or_create(
            character=self.cleaned_data["character"],
            related_to=self.cleaned_data["related_to"],
            defaults=self.cleaned_data,
        )[0]