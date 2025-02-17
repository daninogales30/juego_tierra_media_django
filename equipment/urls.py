from django.urls import path

from equipment import views

app_name = 'equipment'
urlpatterns = [
    path('list/', views.EquipmentListView.as_view(), name='equipment_list'),
    path('add/', views.EquipmentCreateView.as_view(), name='equipment_add'),
    path('delete/<int:pk>/', views.DeleteEquipmentView.as_view(), name='equipment_delete'),
]