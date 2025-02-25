from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from equipment.forms import AssignEquipmentForm

from django.views.generic import ListView
from django.db.models import Q
from .models import Equipment, Weapon


class EquipmentListView(LoginRequiredMixin, ListView, FormView):
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

class AssignEquipmentView(LoginRequiredMixin, FormView):
    form_class = AssignEquipmentForm
    template_name = "assign_equipment.html"
    success_url = reverse_lazy("equipment:equipment_list")

    def form_valid(self, form):
        character = form.cleaned_data['character']
        equipment = form.cleaned_data['equipment']
        character.add_equipment(equipment)

        return super().form_valid(form)

class PotenciaView(ListView):
    model = Weapon
    template_name = 'potencia.html'
    context_object_name = 'weapons'

    def get_queryset(self):
        return Weapon.objects.filter(potencia__gt=30).order_by('alcance')

class AlcanceView(ListView):
    model = Equipment
    template_name = 'alcance.html'
    context_object_name = 'weapons'

    def get_queryset(self):
        query = Q(weapon__isnull=False, weapon__alcance__gt=5)
        return Equipment.objects.filter(query).order_by('name')