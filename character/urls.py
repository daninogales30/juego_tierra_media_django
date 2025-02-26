from rest_framework.decorators import api_view
from rest_framework.response import Response

from character import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from character.views import CharacterViewSet, RelacionViewSet

@api_view(['GET'])
def api_root(request):
    return Response({
        'characters': request.build_absolute_uri('characters/'),
        'relationships': request.build_absolute_uri('relacions/')
    })

router = DefaultRouter()
router.register(r'characters', CharacterViewSet)
router.register(r'relacions', RelacionViewSet)

app_name = 'character'
urlpatterns = [
    path('', views.StartGameView.as_view(), name='start_game'),
    path('api/', include([
        path('', api_root, name='api-root'),
        path('', include(router.urls))
    ])),
    path('character_stats/<int:pk>/', views.CharacterStatsView.as_view(), name='character_stats'),
    path('register/', views.RegistroUsuarioView.as_view(), name='register'),
    path('principal_menu/', views.PrincipalMenuView.as_view(), name='principal_menu'),
    path('delete_character/<int:pk>/', views.DeleteCharacterView.as_view(),name='delete_character'),
    path('detail_character/<int:pk>/', views.DetailCharacterView.as_view(), name='detail_character'),
    path('create_character/', views.CreateCharacterView.as_view(), name='create_character'),
    path('equip_weapon/<int:pk>/', views.EquipWeaponView.as_view(),name='equip_weapon'),
    path('change_ubication/<int:pk>/', views.ChangeUbicationView.as_view(), name='change_ubication'),
    path('character_list/', views.CharacterListView.as_view(), name='character_list'),
    path('relacion_create/', views.RelacionCreateView.as_view(), name="relacion_create"),
    path('humanos_list/', views.HumanosView.as_view(), name="humanos_list"),
    path('humanos_sin_armas/', views.HumanosSinArmaView.as_view(), name="humanos_sin_armas"),
]