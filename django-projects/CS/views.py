from django.shortcuts import render
from .models import *
from django.http import HttpResponse
import subprocess
import os

def service_list(request):
    services = Service.objects.order_by('ServiceName')
    return render(request, 'CS/service_list.html', {'name': 'Alex', 'surname': 'Ivanov', 'email': 'ivanov.alex@gmail.com', 'ip_address': '192.168.1.201', 'services': services})

from django.core.exceptions import ValidationError

def connect(request):
    isClient = Client.objects.filter(ClientEmail = request.GET['email'])
    if not isClient.count:
        Client.objects.create(ClientName = request.GET['name'], ClientSurname = request.GET['surname'], ClientEmail = request.GET['email'])
    c = Client.objects.get(ClientEmail = request.GET['email'])
    s = Service.objects.get(ServiceName = request.GET['service'])
    ClientService.objects.create(ClientId = c.ClientId, ServiceId = s.ServiceId, IpAddress = request.GET['ip_address'])
    #os.system('sudo ./VCLIConfigurator.sh userPortGroup VM1 %s %s' % (request.GET['service'], request.GET['ip_address']))
    return HttpResponse('win!')

def login(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    return render(request, 'CS/login.html', {'email': email, 'password': password})

