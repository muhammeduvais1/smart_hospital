from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('', include('hospital_admin.urls')),
    path('doctors/', include('doctor.urls')),
    path('patients/', include('patient.urls')),
    path('nurses/', include('nurse.urls')),
]
