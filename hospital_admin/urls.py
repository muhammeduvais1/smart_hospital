from django.urls import path
from . import views

app_name = 'hospital_admin'

urlpatterns = [
    path('', views.index, name='index'),
    path('appointments/', views.appointments_list, name='appointments'),
    path('appointments/add/', views.appointment_create, name='appointment_add'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('appointments/json/', views.appointments_json, name='appointments_json'),
    path('calendar/', views.appointments_list, name='calendar'),
    path('records/', views.medical_records_list, name='records'),
    path('records/add/', views.record_create, name='record_add'),
]
