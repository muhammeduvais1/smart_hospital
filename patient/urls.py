from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.create, name='create'),
    path('<int:pk>/edit/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/test-results/', views.test_results_list, name='test_results_list'),
    path('<int:pk>/test-results/add/', views.add_test_result, name='add_test_result'),
    path('<int:pk>/test-results/<int:result_id>/edit/', views.edit_test_result, name='edit_test_result'),
    path('<int:pk>/test-results/<int:result_id>/delete/', views.delete_test_result, name='delete_test_result'),
]

