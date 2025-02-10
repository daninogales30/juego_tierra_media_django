from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView

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
    success_url = reverse_lazy("character_list")

class EquipWeaponView(UpdateView):
    model = Character
    fields = ["arma_equipada"]
    template_name = "equip_weapon.html"
    success_url = reverse_lazy("character_list")

class ChangeUbicationView(UpdateView):
    model = Character
    fields = ["ubication"]
    template_name = "change_ubication.html"
    success_url = reverse_lazy("character_list")

class CharacterListView(ListView):
    model = Character
    template_name = "character_list.html"
    context_object_name = "characters"

class RelacionCreateView(CreateView):
    model = Relacion
    form_class = RelacionForm
    template_name = "relacion_form.html"
    success_url = reverse_lazy("character_list")