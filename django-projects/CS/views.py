from django.shortcuts import render
from .models import *
#from django.shortcuts import render_to_response
from django.http import HttpResponse
#from subprocess import Popen, PIPE
import subprocess
import os

def service_list(request):
    services = Service.objects.order_by('ServiceName')
    return render(request, 'CS/service_list.html', {'name': 'Alex', 'surname': 'Ivanov', 'email': 'ivanov.alex@gmail.com', 'ip_address': '192.168.1.201', 'services': services})

def connect(request):
    #f = open('/home/user/mysite/CS/services', 'a')
        #if 'name' in request.GET:
        #        f.write(request.GET['name'] + ' ')
        #if 'service' in request.GET:
        #        f.write(request.GET['service'] + ' ')
        #if 'ip_address' in request.GET:
        #        f.write(request.GET['ip_address'] + '\n')
    Client.objects.create(ClientName = request.GET['name'], ClientSurname = request.GET['surname'], ClientEmail = request.GET['email'])
    c = Client.objects.get(ClientEmail = request.GET['email'])
    s = Service.objects.get(ServiceName = request.GET['service'])
    ClientService.objects.create(ClientId = c.ClientId,ServiceId = s.ServiceId,IpAddress = request.GET['ip_address'])
    #out, err = Popen('./test.sh', shell=True, stdout=PIPE).communicate()
    #print f >> out
    #f.close()
    #r = subprocess.call("sudo ./test.sh",Shell=True)
    #process = subprocess.Popen(['python', 'manage.py', './test.sh'])
    os.system('sudo ./VCLIConfigurator.sh userPortGroup VM1 %s %s' % (request.GET['service'], request.GET['ip_address']))
    #os.system('./home/user/mysite/CS/test.sh')
    return HttpResponse('win!')

def login(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    return render(request, 'CS/login.html', {'email': email, 'password': password})

