from character import views
from django.urls import path

app_name = 'character'
urlpatterns = [
    path('', views.StartGameView.as_view(), name='start_game'),
    path('register/', views.RegistroUsuarioView.as_view(), name='register'),
    path('principal_menu/', views.PrincipalMenuView.as_view(), name='principal_menu'),
    path('delete_character/<int:pk>/', views.DeleteCharacterView.as_view(),name='delete_character'),
    path('detail_character/<int:pk>/', views.DetailCharacterView.as_view(), name='detail_character'),
    path('create_character/', views.CreateCharacterView.as_view(), name='create_character'),
    path('equip_weapon/<int:pk>/', views.EquipWeaponView.as_view(),name='equip_weapon'),
    path('change_ubication/<int:pk>/', views.ChangeUbicationView.as_view(), name='change_ubication'),
    path('character_list/', views.CharacterListView.as_view(), name='character_list'),
    path('relacion_create/', views.RelacionCreateView.as_view(), name="relacion_create"),
]