from django.urls import path
from . import views

urlpatterns = [
path('', views.admin_home, name='admin_dashboard'),
    path('viaturas', views.admin_viaturas, name='admin_viaturas'),
    path('reservas', views.admin_reservas, name='admin_reservas'),
    path('manutencoes/', views.listar_manutencoes, name='admin_manutencoes'),
    path('manutencoes/criar/', views.criar_manutencao, name='criar_manutencao'),
    path('manutencoes/editar/<int:manutencao_id>/', views.editar_manutencao, name='admin_manutencoes_editar'),
    path("manutencoes/eliminar/<int:id_manutencao>/", views.eliminar_manutencao, name="eliminar_manutencao"),
    path('administracao', views.admin_administracao, name='admin_administracao'),
    path('administracao/marcas', views.admin_marcaslist, name='admin_marcaslist'),
    path('administracao/marcas/create/', views.admin_marcacreate, name='admin_marcacreate'),
    path('administracao/marcas/edit/<int:marcaid>/', views.admin_marcaedit, name='admin_marcaedit'),
    path('marcas/delete/<int:marcaid>/', views.admin_marcadelete, name='admin_marcadelete'),
    path('administracao/modelos/', views.admin_modeloslist, name='admin_modeloslist'),
    path('administracao/modelos/create/', views.admin_modelocreate, name='admin_modelocreate'),
    path('administracao/modelos/edit/<int:modelo_id>/', views.admin_modeloedit, name='admin_modeloedit'),
    path('administracao/modelos/delete/<int:modelo_id>/', views.admin_modelodelete, name='admin_modelodelete'),
]

