from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from equipment.forms import AssignEquipmentForm
from equipment.models import Equipment




class EquipmentListView(ListView, FormView):
    model = Equipment
    template_name = "equipment_list.html"
    context_object_name = "equipments"
    form_class = AssignEquipmentForm
    success_url = reverse_lazy("equipment:equipment_list")

    def form_valid(self, form):
        character = form.cleaned_data['character']
        equipment = form.cleaned_data['equipment']

        character.equipment.add(equipment)
        return redirect(self.success_url)
