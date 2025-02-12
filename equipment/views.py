from django.views.generic import  ListView, DeleteView
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from equipment.models import Equipment
from character.models import Character

TIPO_CHOICES = [
    ('weapon', 'Weapon'),
    ('armor', 'Armor'),
]

class EquipmentForm(forms.ModelForm):
    character = forms.ModelChoiceField(required=False, queryset=Character.objects.none(), label="Asignar a personaje")
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

            if character:
                print(
                    f"Personaje: {character}, Tipo de equipo: {equipment.tipo}, Potencia: {equipment.potencia} añadidos")

            return redirect('equipment_list')
        else:
            return HttpResponse("Error en el formulario. Por favor, revisa los datos.")
    else:
        form = EquipmentForm()
    return render(request, "equipment_form.html", {"form": form})


class EquipmentListView(ListView):
    model = Equipment
    template_name = "equipment_list.html"
    context_object_name = "equipments"


class DeleteEquipmentView(DeleteView):
    model = Equipment
    template_name = "equipment_delete.html"

    def get_success_url(self):
        return reverse('equipment_list')

