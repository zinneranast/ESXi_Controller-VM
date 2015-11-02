from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^services/', views.services, name='services'),
    url(r'^connect/', views.connect, name='connect'),
    url(r'control/', views.control, name='control'),
    url(r'portgroups/', views.portgroups, name='portgroups'),
    url(r'virtmachines/', views.virtmachines, name='virtmachines'),
    url(r'switches/', views.switches, name='switches'),
    url(r'rootcommand/', views.rootcommand, name='rootcommand'),
    url(r'establishconnections/(?P<serviceName>[a-zA-Z0-9]+)/', views.establishconnections, name='establishconnections'),
    url(r'delconnection/(?P<serviceName>[a-zA-Z0-9]+)/(?P<vmName>[a-zA-Z0-9]+)/', views.delconnection, name='delconnection'),
]
