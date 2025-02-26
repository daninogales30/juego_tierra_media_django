from django.views.generic import FormView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Battle
from .forms import BattleForm


class BattleView(LoginRequiredMixin, FormView):
    form_class = BattleForm
    template_name = 'battleview.html'

    def form_valid(self, form):
        char1 = form.cleaned_data['character1']
        char2 = form.cleaned_data['character2']

        if char1 == char2:
            form.add_error(None, "¡No puedes pelear contigo mismo!")
            return self.form_invalid(form)

        battle = Battle.objects.create(character1=char1, character2=char2)
        battle.simulate_battle()

        context = self.get_context_data()
        context['battle'] = battle
        context['history'] = battle.battle_history
        return self.render_to_response(context)