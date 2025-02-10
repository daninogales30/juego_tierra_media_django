
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import Equipment

TIPO_CHOICES = [
    ('weapon', 'Weapon'),
    ('armor', 'Armor'),
]

class EquipmentForm(forms.ModelForm):
    character = forms.ModelChoiceField(required=False, label="Asignar a personaje")
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, widget=forms.Select(), label="Tipo de equipo")

    class Meta:
        model = Equipment
        fields = ['name', 'tipo', 'potencia']
        labels = {
            'name': 'Nombre',
            'tipo': 'Tipo de equipo',
            'potencia': 'Potencia'
        }


def equipment_view(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            character = form.cleaned_data.get('character', None)
            print(f"Personaje: {character}, Arma tipo: {equipment.tipo}, Potencia: {equipment.potencia}, añadidos")
            return HttpResponse("¡Equipo guardado exitosamente!")
        else:
            return HttpResponse("Error en el formulario. Por favor, revisa los datos.")
    else:
        form = EquipmentForm()
    return render(request, "form_equipment.html", {"form": form})

def equipment_list_view(request):
    equipments = Equipment.objects.all()
    return render(request, "equipment_list.html", {"equipments": equipments})

