"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # Importa a função redirect

urlpatterns = [
    path('admin/', include('myapp_administradores.urls')),                                    # URL para o painel admin
    path('administracao/', include('myapp_administradores.urls')),
    path('clientes/', include('myapp_clientes.urls')),                  # URL para a app 'clientes'
    path('login/', include('login.urls')),     # Redireciona a raiz para /clientes/
    path('', lambda request: redirect('login/', permanent=False)),  # Redireciona a raiz para /login/
]
