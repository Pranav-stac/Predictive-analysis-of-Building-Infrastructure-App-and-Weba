# maintenance/views.py
from django.http import HttpResponse

from django.template import loader

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

from django.shortcuts import render

def real_time_monitoring(request):
    return render(request, 'real_time_monitoring.html')

def automated_alerts(request):
    return render(request, 'automated_alerts.html')

def data_analytics(request):
    return render(request, 'data_analytics.html')

def safety_assurance(request):
    return render(request, 'safety_assurance.html')