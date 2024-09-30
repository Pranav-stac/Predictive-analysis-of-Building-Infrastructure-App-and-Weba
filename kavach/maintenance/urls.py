from django.urls import path
from . import views
from .views import upload_pdf, report_page
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComplaintViewSet

router = DefaultRouter()
router.register(r'complaints', ComplaintViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('real_time_monitoring/', views.real_time_monitoring, name='real_time_monitoring'),
    path('automated_alerts/', views.automated_alerts, name='automated_alerts'),
    path('data_analytics/', views.data_analytics, name='data_analytics'),
    path('api/', include(router.urls)),
    path('safety_assurance/', views.safety_assurance, name='safety_assurance'),
    
    # ... other URL patterns ...
    # path('upload/', views.upload_pdf, name='upload'),
    path('report_page/', views.report_page, name='report_page'),
    path('upload_pdf/', upload_pdf, name='upload_pdf'),
    path('complaint/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('upload-complaint/', views.upload_complaint, name='upload_complaint'),
    
]
