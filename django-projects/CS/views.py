from django.shortcuts import render
from .models import *
from django.http import HttpResponse
import subprocess
import os

def services(request):
    services = Service.objects.order_by('ServiceName')
    return render(request, 'CS/services.html', {'name': 'Alex', 'surname': 'Ivanov', 'email': 'ivanov.alex@gmail.com', 'ip_address': '192.168.1.201', 'services': services})

def connect(request):
    isClientExists = Client.objects.filter(ClientEmail = request.GET['email'])
    if not isClientExists.count():
        client = Client(ClientName = request.GET['name'], ClientSurname = request.GET['surname'], ClientEmail = request.GET['email'])
        client.save()

    c = Client.objects.get(ClientEmail = request.GET['email'])
    s = Service.objects.get(ServiceName = request.GET['service'])

    ClientService.objects.create(ClientId = c.ClientId, ServiceId = s.ServiceId, IpAddress = request.GET['ip_address'])
    #os.system('sudo ./VCLIConfigurator.sh userPortGroup VM1 %s %s' % (request.GET['service'], request.GET['ip_address']))
    return HttpResponse('The service was connected succesfully.')

def login(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    return render(request, 'CS/login.html', {'email': email, 'password': password})

def control(request):
    return render(request, 'CS/control.html')

def portgroups(request):
    getPortGroups = subprocess.Popen("esxcli -c sessionConfig.cfg network vswitch standard portgroup list", shell=True, stdout=subprocess.PIPE)
    portGroups = getPortGroups.stdout.readlines()
    return render(request, 'CS/portgroups.html', {'portGroups': portGroups})

def virtmachines(request):
    getVirtMachines = subprocess.Popen("vmware-cmd --config sessionConfig.cfg -l", shell=True, stdout=subprocess.PIPE)
    virtMachines = getVirtMachines.stdout.readlines()
    return render(request, 'CS/virtmachines.html', {'virtMachines': virtMachines})

