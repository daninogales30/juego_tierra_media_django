from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView

from battle.forms import BattleForm
from battle.models import Battle



# Create your views here.
class BattleView(LoginRequiredMixin, FormView):
    form_class = BattleForm
    template_name = 'battleview.html'

    def form_valid(self, form):
        jugador1 = form.cleaned_data['jugador1']
        jugador2 = form.cleaned_data['jugador2']

        if jugador1 == jugador2:
            form.add_error("jugador1", "No se puede pelear con el mismo personaje")
            return self.form_invalid(form)

        if not jugador1.arma_equipada or not jugador2.arma_equipada:
            form.add_error("jugador1", "Se necesita equipar un arma en ambos personajes")
            return self.form_invalid(form)

        batalla = Battle.objects.create(character1=jugador1, character2=jugador2)
        try:
            batalla.simulate()
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

        jugador1.refresh_from_db()
        jugador2.refresh_from_db()

        # Convertir el log en lista para el template

        return render(self.request, 'battleview.html', {
            'form': form,
            'battle': batalla,
            'character1': jugador1,
            'character2': jugador2,
            'loser': batalla.loser
        })