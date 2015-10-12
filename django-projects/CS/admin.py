from django.contrib import admin
from .models import Client, Service, ClientService

admin.site.register(Client)
admin.site.register(Service)
admin.site.register(ClientService)
