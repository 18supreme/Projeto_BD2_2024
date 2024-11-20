from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes_home, name='clientes_home'),
    path('viaturas/', views.viaturas_list, name='viaturas_list'),
    path('viatura/<int:id>/', views.viatura_detail, name='viatura_detail'),
]
