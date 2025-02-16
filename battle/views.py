from django.utils import timezone

from django.shortcuts import render
from django.views.generic import FormView

from battle.forms import BattleForm
from battle.models import Battle


# Create your views here.
class BattleView(FormView):
    form_class = BattleForm
    template_name = 'battleview.html'

    def form_valid(self, form):
        personaje1 = form.cleaned_data['personaje1']
        personaje2 = form.cleaned_data['personaje2']

        batalla = Battle.objects.create(character1=personaje1, character2=personaje2)
        batalla.simulate()

        return render(self.request, 'battleview.html', {'form': form, 'ganador': batalla.winner})