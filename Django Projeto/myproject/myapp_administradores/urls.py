from django.urls import path
from . import views

urlpatterns = [
path('', views.admin_home, name='admin_dashboard'),
    # ---| Viaturas |---
    path('viaturas', views.admin_viaturas, name='admin_viaturas'),
    path('viaturas/criar/', views.admin_viaturas_create, name='admin_viaturas_create'),
    path('viaturas/editar/<int:viatura_id>/', views.admin_viaturas_edit, name='admin_viaturas_edit'),
    path('administracao/viaturas/delete/<int:viatura_id>/', views.admin_viaturas_delete, name='admin_viaturas_delete'),
    # ---| Reservas |---
    path('reservas', views.admin_reservas, name='admin_reservas'),
    path('reservas/create/', views.admin_reservas_create, name='admin_reservas_create'),
    path('reservas/edit/<int:reserva_id>/', views.admin_reservas_edit, name='admin_reservas_edit'),
    path('reservas/delete/<int:reserva_id>/', views.admin_reservas_delete, name='admin_reservas_delete'),
    # ---| Manutenções |---
    path('manutencoes/', views.listar_manutencoes, name='admin_manutencoes'),
    path('manutencoes/criar/', views.criar_manutencao, name='criar_manutencao'),
    path('manutencoes/editar/<int:manutencao_id>/', views.editar_manutencao, name='admin_manutencoes_editar'),
    path("manutencoes/eliminar/<int:id_manutencao>/", views.eliminar_manutencao, name="eliminar_manutencao"),
    # ---| Marcas |---
    path('administracao', views.admin_administracao, name='admin_administracao'),
    path('administracao/marcas', views.admin_marcaslist, name='admin_marcaslist'),
    path('administracao/marcas/create/', views.admin_marcacreate, name='admin_marcacreate'),
    path('administracao/marcas/edit/<int:marcaid>/', views.admin_marcaedit, name='admin_marcaedit'),
    path('marcas/delete/<int:marcaid>/', views.admin_marcadelete, name='admin_marcadelete'),
    # ---| Modelos |---
    path('administracao/modelos/', views.admin_modeloslist, name='admin_modeloslist'),
    path('administracao/modelos/create/', views.admin_modelocreate, name='admin_modelocreate'),
    path('administracao/modelos/edit/<int:modelo_id>/', views.admin_modeloedit, name='admin_modeloedit'),
    path('administracao/modelos/delete/<int:modelo_id>/', views.admin_modelodelete, name='admin_modelodelete'),
    # ---| Cores |---
    path('administracao/cores/', views.admin_coreslist, name='admin_coreslist'),
    path('administracao/cores/create/', views.admin_corcreate, name='admin_corcreate'),
    path('administracao/cores/edit/<int:cor_id>/', views.admin_coredit, name='admin_coredit'),
    path('administracao/cores/delete/<int:cor_id>/', views.admin_cordelete, name='admin_cordelete'),
    # ---| Combustivel |---
    path('administracao/combustiveis/', views.admin_combustiveislist, name='admin_combustiveislist'),
    path('administracao/combustiveis/create/', views.admin_combustivelcreate, name='admin_combustivelcreate'),
    path('administracao/combustiveis/edit/<int:combustivel_id>/', views.admin_combustiveledit, name='admin_combustiveledit'),
    path('administracao/combustiveis/delete/<int:combustivel_id>/', views.admin_combustiveldelete, name='admin_combustiveldelete'),
    # ---| Fornecedores |---
    path('administracao/fornecedores/', views.admin_fornecedoreslist, name='admin_fornecedoreslist'),
    path('administracao/fornecedores/create/', views.admin_fornecedorcreate, name='admin_fornecedorcreate'),
    path('administracao/fornecedores/delete/<int:fornecedor_id>/', views.admin_fornecedordelete, name='admin_fornecedordelete'),
    path('administracao/fornecedores/edit/<int:fornecedor_id>/', views.admin_fornecedoredit, name='admin_fornecedoredit'),
    # ---| Encomendas |---
    path('administracao/encomendas/', views.admin_encomendaslist, name='admin_encomendaslist'),
    path('administracao/encomendas/create/', views.admin_encomendacreate, name='admin_encomendacreate'),
    path('administracao/encomendas/edit/<int:encomenda_id>/', views.admin_encomendaedit, name='admin_encomendaedit'),
    path('administracao/encomendas/delete/<int:encomenda_id>/', views.admin_encomendadelete, name='admin_encomendadelete'),
    # ---| Peças |---
    path("administracao/pecas/", views.admin_pecaslist, name="admin_pecaslist"),
    path("administracao/pecas/create/", views.admin_pecacreate, name="admin_pecacreate"),
    path("administracao/pecas/edit/<int:peca_id>/", views.admin_pecaedit, name="admin_pecaedit"),
    path("administracao/pecas/delete/<int:peca_id>/", views.admin_pecadelete, name="admin_pecadelete"),
    # ---| Utilizadores |---
    path("administracao/utilizadores/", views.admin_utilizadoreslist, name="admin_utilizadoreslist"),
    path("administracao/utilizadores/create/", views.admin_utilizadorcreate, name="admin_utilizadorcreate"),
    path("administracao/utilizadores/edit/<int:utilizador_id>/", views.admin_utilizadoredit, name="admin_utilizadoredit"),
    path("administracao/utilizadores/delete/<int:utilizador_id>/", views.admin_utilizadordelete, name="admin_utilizadordelete"),
]