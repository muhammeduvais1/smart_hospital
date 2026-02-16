from django.urls import path
from . import views

app_name = 'nurse'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.create, name='create'),
    path('<int:pk>/edit/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
