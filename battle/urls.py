from battle import views
from django.urls import path

app_name = 'battle'
urlpatterns = [
    path('', views.BattleView.as_view(), name='simulate'),
]