from django.urls import path
from .views import EquipmentListView, DeleteEquipmentView, equipment_view
urlpatterns = [
    path('list/', EquipmentListView, name='equipment_list'),
    path('add/', equipment_view, name='equipment_add'),
    path('delete/<int:pk>/', DeleteEquipmentView, name='equipment_delete'),
]