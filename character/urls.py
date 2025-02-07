from character import views
from django.urls import path

app_name = 'character'
urlpatterns = [
    path('', views.StartGameView.as_view(), name='StartGame'),
]