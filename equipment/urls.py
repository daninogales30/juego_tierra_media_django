from django.urls import path
from equipment import views

app_name = 'equipment'
urlpatterns = [
    path('', views.CreateEquipment.as_view(), name='CreateEquipment'),
]