from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('real_time_monitoring/', views.real_time_monitoring, name='real_time_monitoring'),
    path('automated_alerts/', views.automated_alerts, name='automated_alerts'),
    path('data_analytics/', views.data_analytics, name='data_analytics'),
    path('safety_assurance/', views.safety_assurance, name='safety_assurance'),
    
    # ... other URL patterns ...
]