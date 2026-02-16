from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.create, name='create'),
    path('<int:pk>/edit/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/availability/', views.availability_list, name='availability_list'),
    path('<int:pk>/availability/add/', views.availability_create, name='availability_create'),
    path('<int:pk>/availability/<int:avail_pk>/delete/', views.availability_delete, name='availability_delete'),
]
