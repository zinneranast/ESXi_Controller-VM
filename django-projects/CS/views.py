from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
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
    #name = request.GET['name']
    #if name is None: # or request.GET['surname'] is None or request.GET['email'] is None or request.GET['ip_address'] is None:
    #    return redirect(request, 'services.html', {'name': 'Alex', 'surname': 'Ivanov', 'email': 'ivanov.alex@gmail.com', 'ip_address': '192.168.1.201', 'services': services, 'empty_field': 'Please fill all of fields.'}, context_instance=RequestContext(request))
    #else:
    #    return redirect(request, '/', {'name': 'Alex', 'surname': 'Ivanov', 'email': 'ivanov.alex@gmail.com', 'ip_address': '192.168.1.201', 'services': services, 'empty_field': 'ok.'})
        
    ifClientExists = Client.objects.filter(ClientEmail = request.GET['email'])
    if not ifClientExists.count():
        client = Client(ClientName = request.GET['name'], ClientSurname = request.GET['surname'], ClientEmail = request.GET['email'])
        client.save()

    c = Client.objects.get(ClientEmail = request.GET['email'])
    s = Service.objects.get(ServiceName = request.GET['service'])

    ifClientServiceExists = ClientService.objects.filter(ClientId = c.ClientId, ServiceId = s.ServiceId, IpAddress = request.GET['ip_address'])
    if not ifClientServiceExists.count():
        clientService = ClientService(ClientId = c.ClientId, ServiceId = s.ServiceId, IpAddress = request.GET['ip_address'])
        clientService.save()

    os.system('sudo ./VCLIConfigurator.sh userPortGroup VM1 %s %s' % (request.GET['service'], request.GET['ip_address']))
    return render(request, 'connect.html')

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

def switches(request):
    getSwitches = subprocess.Popen("vicfg-vswitch --config sessionConfig.cfg -l", shell=True, stdout=subprocess.PIPE)
    switches = getSwitches.stdout.readlines()
    return render(request, 'switches.html', {'switches': switches, 'username': auth.get_user(request).username})

def rootcommand(request):
    getCommand = subprocess.Popen(request.GET['command'], shell=True, stdout=subprocess.PIPE)
    output_command = getCommand.stdout.readlines()
    return render(request, 'rootcommand.html', {'output_command': output_command, 'username': auth.get_user(request).username})

def establishconnections(request, serviceName):
    getServices = subprocess.Popen("sudo ./findService.sh %s | sed 1,4d | sed '$d'" % serviceName, shell=True, stdout=subprocess.PIPE)
    connections = getServices.stdout.readlines()
    connection_fields = []
    for i in connections:
        fields = i.strip().split()
        connection_fields.append(fields)
    return render(request, 'establish-connections.html', {'serviceName': serviceName, 'connections': connection_fields, 'username': auth.get_user(request).username})

def delconnection(request, serviceName, vmName):
    os.system("sudo ./stopService.sh %s %s" % (serviceName, vmName))
    return render(request, 'delconnection.html', {'username': auth.get_user(request).username})
