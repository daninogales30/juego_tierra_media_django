from django.views.generic import ListView, DeleteView, CreateView
from django import forms
from django.urls import reverse, reverse_lazy
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


class EquipmentCreateView(CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = "equipment_form.html"
    success_url = reverse_lazy('equipment_list')

    def form_valid(self, form):
        equipment = form.save()
        character = form.cleaned_data.get('character', None)
        if character:
            print(f"Personaje : {character},Tipo de equipo : {equipment.tipo},Potencia : {equipment.potencia} estan añadidos")

        return super().form_valid(form)

class EquipmentListView(ListView):
    model = Equipment
    template_name = "equipment_list.html"
    context_object_name = "equipments"


class DeleteEquipmentView(DeleteView):
    model = Equipment
    template_name = "equipment_delete.html"

    def get_success_url(self):
        return reverse('equipment_list')

