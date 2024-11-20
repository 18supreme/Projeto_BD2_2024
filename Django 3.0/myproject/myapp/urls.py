from django.urls import path
from . import views

urlpatterns = [
    path('', views.curso_list, name='curso_list'),
    path('new/', views.curso_create, name='curso_create'),
    path('<int:pk>/', views.curso_detail, name='curso_detail'),
    path('<int:pk>/edit/', views.curso_update, name='curso_update'),
    path('<int:pk>/delete/', views.curso_delete, name='curso_delete'),
]
