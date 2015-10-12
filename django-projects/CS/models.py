from django.db import models

class Client(models.Model):
    ClientId = models.AutoField(primary_key=True)
    ClientName = models.CharField(max_length=50)
    ClientSurname = models.CharField(max_length=50)
    ClientEmail = models.CharField(max_length=50)

class Service(models.Model):
    ServiceId = models.AutoField(primary_key=True)
    ServiceName = models.CharField(max_length=50)
    ServiceDescription = models.TextField()

class ClientService(models.Model):
    ClientId = models.CharField(max_length=100)
    ServiceId = models.CharField(max_length=100)
    IpAddress = models.GenericIPAddressField(protocol='IPv4', null=True)
