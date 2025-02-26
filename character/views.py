from django.shortcuts import render

from character.forms import CharacterForm, RelacionForm
from character.models import Character, Relacion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView, DeleteView
from rest_framework.decorators import action
from rest_framework.response import Response
from character.forms import CharacterForm, RelacionForm
from character.models import Relacion
from rest_framework import viewsets
from rest_framework import filters
from character.models import Character
from .serializers import RelacionSerializer, CharacterSerializer

class RelacionViewSet(viewsets.ModelViewSet):
    queryset = Relacion.objects.all()
    serializer_class = RelacionSerializer

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'faction']

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        character = self.get_object()
        return Response({
            "total_equipment": character.equipment.count(),
            "current_weapon_power": character.arma_equipada.potencia if character.arma_equipada else 0,
            "relationships_count": Relacion.objects.filter(character=character).count()
        })


class CharacterStatsView(TemplateView):
    template_name = 'character_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['character_id'] = self.kwargs['pk']
        return context


class RegistroUsuarioView(CreateView):
    template_name = "registration/registro.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("character:start_game")

class StartGameView(LoginRequiredMixin, TemplateView):
    template_name = "start_game.html"

class PrincipalMenuView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

class CreateCharacterView(LoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm
    template_name = "character_form.html"
    success_url = reverse_lazy("character:character_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear Personaje"
        context["subtitle"] = "Crear Nuevo Personaje"
        context["button_text"] = "Guardar"
        return context

class DeleteCharacterView(LoginRequiredMixin, DeleteView):
    model = Character
    template_name = "character_delete.html"
    success_url = reverse_lazy("character:character_list")

class DetailCharacterView(LoginRequiredMixin, DetailView):
    model = Character
    template_name = "character_detail.html"
    context_object_name = "character"

class EquipWeaponView(LoginRequiredMixin, UpdateView):
    model = Character
    fields = ["arma_equipada"]
    template_name = "character_form.html"
    success_url = reverse_lazy("character:character_list")

    def form_valid(self, form):
        character = form.instance
        weapon = form.cleaned_data.get("arma_equipada")

        if weapon and weapon not in character.equipment.all():
            form.add_error("arma_equipada", "No puedes equipar un arma que no posees.")
            return self.form_invalid(form)

        if weapon:
            character.equip_weapon(weapon)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Equipar arma"
        context["subtitle"] = "Equipar un arma"
        context["button_text"] = "Equipar"
        return context

class ChangeUbicationView(LoginRequiredMixin, UpdateView):
    model = Character
    fields = ["ubication"]
    template_name = "character_form.html"
    success_url = reverse_lazy("character:character_list")

    def form_valid(self, form):
        new_ubication = form.cleaned_data.get("ubication")
        character = self.get_object()

        if len(new_ubication) < 3:
            form.add_error("ubication", "La ubicación debe tener al menos 3 caracteres.")
            return self.form_invalid(form)

        if new_ubication == character.ubication:
            form.add_error("ubication", "El personaje ya se encuentra en esta ubicación.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Cambiar ubicación"
        context["subtitle"] = "Cambiar ubicación"
        context["button_text"] = "Cambiar"
        return context
class RelacionCreateView(LoginRequiredMixin, CreateView):
    model = Relacion
    form_class = RelacionForm
    template_name = "relacion_form.html"
    success_url = reverse_lazy("character:character_list")

class CharacterListView(LoginRequiredMixin, ListView):
    model = Character
    template_name = "character_list.html"
    context_object_name = "characters"

class HumanosView(ListView):
    model = Character
    template_name = 'humanos_list.html'
    context_object_name = 'humanos'

    def get_queryset(self):
        return Character.objects.filter(race='humana')

class HumanosSinArmaView(ListView):
    model = Character
    template_name = 'humanos_sin_arma.html'
    context_object_name = 'humanos'

    def get_queryset(self):
        return Character.objects.filter(
            race='humana',
            arma_equipada__isnull=True
        ).order_by('name')