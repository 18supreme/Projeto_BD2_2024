from django.urls import path
from . import views

urlpatterns = [
path('', views.admin_home, name='admin_dashboard'),
    path('viaturas', views.admin_viaturas, name='admin_viaturas'),
    path('reservas', views.admin_reservas, name='admin_reservas'),
    path('manutencoes', views.admin_manutencoes, name='admin_manutencoes'),
    path('manutencoes/create/', views.create_manutencao, name='admin_manutencao_create'),
    path('administracao', views.admin_administracao, name='admin_administracao'),
    path('administracao/marcas', views.admin_marcaslist, name='admin_marcaslist'),
    path('administracao/marcas/create/', views.admin_marcacreate, name='admin_marcacreate'),
    path('administracao/marcas/edit/<int:marcaid>/', views.admin_marcaedit, name='admin_marcaedit'),
    path('marcas/delete/<int:marcaid>/', views.admin_marcadelete, name='admin_marcadelete'),
]
