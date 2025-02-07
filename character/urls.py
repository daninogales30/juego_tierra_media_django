from character import views
from django.urls import path
urlpatterns = [
    path('', views.StartGameView.as_view(), name='StartGame'),
]