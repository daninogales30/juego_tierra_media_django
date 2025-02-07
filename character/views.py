from django.views.generic import TemplateView


class StartGameView(TemplateView):
    template_name = "start_game.html"

class PrincipalMenuView(TemplateView):
    template_name = "index.html"