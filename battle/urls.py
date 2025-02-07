from django.urls import path
from equipment import views

app_name = 'battle'
urlpatterns = [
    path('', views.SimulateBattle.as_view(), name='SimulateBattle'),
]