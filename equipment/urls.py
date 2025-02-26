from django.urls import path

from equipment import views

app_name = 'equipment'
urlpatterns = [
    path('list/', views.EquipmentListView.as_view(), name='equipment_list'),
    path('assign/',views.AssignEquipmentView.as_view(), name='assign_equipment'),
    path('potencia/',views.PotenciaView.as_view(), name='potencia'),
    path('alcance/',views.AlcanceView.as_view(), name='alcance'),
]