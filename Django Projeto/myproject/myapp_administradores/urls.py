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
    path('administracao/cores/', views.admin_coreslist, name='admin_coreslist'),
    path('administracao/cores/create/', views.admin_corcreate, name='admin_corcreate'),
    path('administracao/cores/edit/<int:cor_id>/', views.admin_coredit, name='admin_coredit'),
    path('administracao/cores/delete/<int:cor_id>/', views.admin_cordelete, name='admin_cordelete'),
    path('administracao/combustiveis/', views.admin_combustiveislist, name='admin_combustiveislist'),
    path('administracao/combustiveis/create/', views.admin_combustivelcreate, name='admin_combustivelcreate'),
    path('administracao/combustiveis/edit/<int:combustivel_id>/', views.admin_combustiveledit, name='admin_combustiveledit'),
    path('administracao/combustiveis/delete/<int:combustivel_id>/', views.admin_combustiveldelete, name='admin_combustiveldelete'),
    path('administracao/fornecedores/', views.admin_fornecedoreslist, name='admin_fornecedoreslist'),
    path('administracao/fornecedores/create/', views.admin_fornecedorcreate, name='admin_fornecedorcreate'),
    path('administracao/fornecedores/delete/<int:fornecedor_id>/', views.admin_fornecedordelete, name='admin_fornecedordelete'),
    path('administracao/fornecedores/edit/<int:fornecedor_id>/', views.admin_fornecedoredit, name='admin_fornecedoredit'),
    
]

