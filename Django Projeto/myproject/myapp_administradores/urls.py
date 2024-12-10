from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('/viaturas', views.admin_viaturas, name='admin_viaturas'),
    path('/reservas', views.admin_reservas, name='admin_reservas'),
    path('/manutencoes', views.admin_manutencoes, name='admin_manutencoes'),
    path('/administracao', views.admin_administracao, name='admin_administracao'),
]
