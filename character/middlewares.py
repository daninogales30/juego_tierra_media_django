class LuckyPlayerMiddleware:
    """
    Middleware que da ventaja aleatoria a los jugadores que usan palabras clave en su user-agent
    Ejemplo de user-agent: "LuchadorLegendario v2.1"
    Palabras clave: ["epico", "legendario", "invicto", "dragón"]
    """

    LUCKY_KEYWORDS = ['epico', 'legendario', 'invicto', 'dragón', 'mitico', 'guerrero']
    LUCK_PROBABILITY = 0.3  # 30% de probabilidad de ventaja

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

        # Verificar si el usuario tiene suerte
        if any(keyword in user_agent for keyword in self.LUCKY_KEYWORDS):
            if random.random() < self.LUCK_PROBABILITY:
                request.session['lucky_player'] = True
                request.session['attack_bonus'] = 1.2  # +20% de daño

        response = self.get_response(request)

        # Limpiar la suerte después de cada petición
        if 'lucky_player' in request.session:
            del request.session['lucky_player']

        return response