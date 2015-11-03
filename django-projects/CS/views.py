from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib import auth
from .models import *
import subprocess
import os

def services(request):
    services = Service.objects.order_by('ServiceName')
    getVirtMachines = subprocess.Popen('esxcli --config sessionConfig.cfg vm process list | sed -n "1~8p" | sed "/NAS-server/d"', shell=True, stdout=subprocess.PIPE)
    virtMachines = getVirtMachines.stdout.readlines()
    return render(request, 'services.html', {'surname': 'ivanovalex', 'email': 'ivanov.alex@gmail.com', 'ip_address': '192.168.1.201', 'services': services, 'virt_machines': virtMachines, 'username': auth.get_user(request).username})

def index(request):
    return render(request, 'index.html', {'username': auth.get_user(request).username}) #, context_instance=RequestContext(request))

def connect(request):
    if request.user.is_authenticated():
        username = request.user.username
        email = request.user.email
    else:
        username = request.GET['username']
        email = request.GET['email']

    ifClientExists = Client.objects.filter(ClientEmail = email)
    if not ifClientExists.count():
        client = Client(ClientUsername = username, ClientEmail = email)
        client.save()

    c = Client.objects.get(ClientEmail = email)
    s = Service.objects.get(ServiceName = request.GET['service'])

    ifClientServiceExists = ClientService.objects.filter(ClientId = c.ClientId, ServiceId = s.ServiceId)
    if not ifClientServiceExists.count():
        clientService = ClientService(ClientId = c.ClientId, ServiceId = s.ServiceId, IpAddress = request.GET['ip_address'], ConnectionState = 0)
        clientService.save()

    ifServiceDisconnected = ClientService.objects.filter(ClientId = c.ClientId, ServiceId = s.ServiceId, IpAddress = request.GET['ip_address'], ConnectionState = 0)
    if ifServiceDisconnected.count():
        cs = ClientService.objects.get(ClientId = c.ClientId, ServiceId = s.ServiceId, IpAddress = request.GET['ip_address'])
        cs.ConnectionState = 1
        cs.save()
        if request.GET['virt_machine']:
            os.system('sudo ./VCLIConfigurator.sh userPortGroup %s %s %s %s' % (request.GET['virt_machine'], request.GET['service'], request.GET['ip_address'], username))
        else:
            os.system('sudo ./VCLIConfigurator.sh userPortGroup VM1 %s %s %s' % (request.GET['service'], request.GET['ip_address'], username))
        return render(request, 'connect.html', {'username': username})
    else:
        return HttpResponse('This service is already connected!')

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
    if request.user.is_superuser:
        getServices = subprocess.Popen("sudo ./findService.sh %s root | sed 1,4d | sed '$d'" % serviceName, shell=True, stdout=subprocess.PIPE)
    else:
        getServices = subprocess.Popen("sudo ./findService.sh %s %s | sed 1,4d | sed '$d'" % (serviceName, auth.get_user(request).username), shell=True, stdout=subprocess.PIPE)
    connections = getServices.stdout.readlines()
    connection_fields = []
    for i in connections:
        fields = i.strip().split()
        connection_fields.append(fields)
    return render(request, 'establish-connections.html', {'serviceName': serviceName, 'connections': connection_fields, 'username': auth.get_user(request).username})

def delconnection(request, serviceName, vmName, userName):
    c = Client.objects.get(ClientUsername = userName)
    s = Service.objects.get(ServiceName = serviceName)

    cs = ClientService.objects.get(ClientId = c.ClientId, ServiceId = s.ServiceId)
    cs.ConnectionState = 0
    cs.save()    
    os.system("sudo ./stopService.sh %s %s %s" % (serviceName, vmName, userName))
    return render(request, 'delconnection.html', {'message': 'The service is succesfully disconnected.', 'username': auth.get_user(request).username})

def delconnectionall(request):
    ClientService.objects.all().delete()
    os.system("sudo ./stopService.sh")
    return render(request, 'delconnection.html', {'message': 'All connections are succesfully deleted.', 'username': auth.get_user(request).username})

