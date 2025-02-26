from django.views.generic import FormView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Battle
from .forms import BattleForm


class BattleView(LoginRequiredMixin, FormView):
    form_class = BattleForm
    template_name = 'battleview.html'

    def form_valid(self, form):
        character1 = form.cleaned_data['character1']
        character2 = form.cleaned_data['character2']

        if character2 == character1:
            form.add_error(None, "¡No puedes pelear contigo mismo!")
            return self.form_invalid(form)

        battle = Battle.objects.create(character1=character1, character2=character2)
        battle.simulate_battle()

        context = self.get_context_data()
        context['battle'] = battle
        context['history'] = battle.battle_history
        return self.render_to_response(context)