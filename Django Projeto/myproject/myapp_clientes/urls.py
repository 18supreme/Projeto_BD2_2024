from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes_home, name='clientes_home'),
    path('viaturas/', views.viaturas_list, name='viaturas_list'),
    path('viatura/<int:id>/', views.viatura_detail, name='viatura_detail'),
    path('reservas/', views.reservas_list, name='reservas_list'),
    path('viatura/<int:id>/criar_reserva', views.criar_reserva, name='criar_reserva')
]
