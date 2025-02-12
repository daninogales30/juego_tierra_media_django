from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView, DeleteView

from character.forms import CharacterForm, RelacionForm
from character.models import Character, Relacion


class StartGameView(TemplateView):
    template_name = "start_game.html"

class PrincipalMenuView(TemplateView):
    template_name = "index.html"

class CreateCharacterView(CreateView):
    model = Character
    form_class = CharacterForm
    template_name = "character_form.html"
    success_url = reverse_lazy("character:character_list")

class DeleteCharacterView(DeleteView):
    model = Character
    template_name = "character_delete.html"
    success_url = reverse_lazy("character:character_list")

class DetailCharacterView(DetailView):
    model = Character
    template_name = "character_detail.html"
    context_object_name = "character"

class EquipWeaponView(UpdateView):
    model = Character
    fields = ["arma_equipada"]
    template_name = "character_form.html"
    success_url = reverse_lazy("character:character_list")

    def form_valid(self, form):
        character = form.instance
        weapon = form.cleaned_data["arma_equipada"]

        if weapon and weapon not in character.equipment.all():
            return HttpResponseBadRequest("No puedes equipar un arma que no posees.")

        return super().form_valid(form)

class ChangeUbicationView(UpdateView):
    model = Character
    fields = ["ubication"]
    template_name = "character_form.html"
    success_url = reverse_lazy("character:character_list")

    def form_valid(self, form):
        new_ubication = form.cleaned_data["ubication"]
        character = self.get_object()  # Obtener la instancia actual del personaje

        if len(new_ubication) < 3:
            return HttpResponseBadRequest("La ubicación debe tener al menos 3 caracteres.")

        if new_ubication == character.ubication:
            return HttpResponseBadRequest("El personaje ya se encuentra en esta ubicación.")

        return super().form_valid(form)


class RelacionCreateView(CreateView):
    model = Relacion
    form_class = RelacionForm
    template_name = "relacion_form.html"
    success_url = reverse_lazy("character:character_list")

class CharacterListView(ListView):
    model = Character
    template_name = "character_list.html"
    context_object_name = "characters"
