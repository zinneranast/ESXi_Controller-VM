from django.shortcuts import render
from django.template import RequestContext
from django.contrib import auth
from .models import *
import subprocess
import os

def services(request):
    services = Service.objects.order_by('ServiceName')
    return render(request, 'services.html', {'name': 'Alex', 'surname': 'Ivanov', 'email': 'ivanov.alex@gmail.com', 'ip_address': '192.168.1.201', 'services': services, 'username': auth.get_user(request).username})

def index(request):
    return render(request, 'index.html', {'username': auth.get_user(request).username}) #, context_instance=RequestContext(request))

def connect(request):
    isClientExists = Client.objects.filter(ClientEmail = request.GET['email'])
    if not isClientExists.count():
        client = Client(ClientName = request.GET['name'], ClientSurname = request.GET['surname'], ClientEmail = request.GET['email'])
        client.save()

    c = Client.objects.get(ClientEmail = request.GET['email'])
    s = Service.objects.get(ServiceName = request.GET['service'])

    ClientService.objects.create(ClientId = c.ClientId, ServiceId = s.ServiceId, IpAddress = request.GET['ip_address'])
    #os.system('sudo ./VCLIConfigurator.sh userPortGroup VM1 %s %s' % (request.GET['service'], request.GET['ip_address']))
    return render(request, 'connect.html')
    #return HttpResponse("ura!")

def control(request):
    return render(request, 'control.html', {'username': auth.get_user(request).username})

def portgroups(request):
    getPortGroups = subprocess.Popen("esxcli -c sessionConfig.cfg network vswitch standard portgroup list", shell=True, stdout=subprocess.PIPE)
    portGroups = getPortGroups.stdout.readlines()
    return render(request, 'portgroups.html', {'port_groups': portGroups, 'username': auth.get_user(request).username})

def virtmachines(request):
    getVirtMachines = subprocess.Popen("vmware-cmd --config sessionConfig.cfg -l", shell=True, stdout=subprocess.PIPE)
    virtMachines = getVirtMachines.stdout.readlines()
    return render(request, 'virtmachines.html', {'virt_machines': virtMachines, 'username': auth.get_user(request).username})

