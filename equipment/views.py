from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from equipment.forms import AssignEquipmentForm
from equipment.models import Equipment




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

class AssignEquipmentView(LoginRequiredMixin, View):
    template_name = "assign_equipment.html"

    def get(self, request):
        form = AssignEquipmentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AssignEquipmentForm(request.POST)
        if form.is_valid():
            character = form.cleaned_data['character']
            equipment = form.cleaned_data['equipment']
            character.equipment.add(equipment)
            character.save()
            return redirect('equipment:equipment_list')
        return render(request, self.template_name, {'form': form})
