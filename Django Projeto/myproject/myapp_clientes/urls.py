from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes_home, name='clientes_home'),
    path('viaturas/', views.viaturas_list, name='viaturas_list'),
    path('viatura/<int:id>/', views.viatura_detail, name='viatura_detail'),
    path('reservas/', views.reservas_list, name='reservas_list'),
    path('viatura/<int:viatura_id>/criar_reserva', views.criar_reserva, name='criar_reserva'),
    path('reservas/cancelar/<int:reserva_id>/', views.reserva_cancelar, name='cancelar_reserva'),
    path('reservas/entregar/<int:reserva_id>/', views.reserva_entregar, name='entregar_reserva'),
]
