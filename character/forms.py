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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["character"].queryset = Character.objects.all()
        self.fields["related_to"].queryset = Character.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        character = cleaned_data.get("character")
        related_to = cleaned_data.get("related_to")

        if character == related_to:
            raise forms.ValidationError("Un personaje no puede relacionarse consigo mismo.")

        return cleaned_data