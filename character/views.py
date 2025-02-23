from django.http import HttpResponseBadRequest
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
        weapon = form.cleaned_data.get("arma_equipada")

        if weapon and weapon not in character.equipment.all():
            form.add_error("arma_equipada", "No puedes equipar un arma que no posees.")
            return self.form_invalid(form)

        if weapon:
            character.equip_weapon(weapon)

        return super().form_valid(form)


class ChangeUbicationView(UpdateView):
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

class RelacionCreateView(CreateView):
    model = Relacion
    form_class = RelacionForm
    template_name = "relacion_form.html"
    success_url = reverse_lazy("character:character_list")

class CharacterListView(ListView):
    model = Character
    template_name = "character_list.html"
    context_object_name = "characters"
