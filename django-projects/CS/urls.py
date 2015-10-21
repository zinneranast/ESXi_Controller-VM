from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^services/', views.services, name='services'),
    url(r'^connect/', views.connect, name='connect'),
    url(r'control/', views.control, name='control'),
    url(r'portgroups/', views.portgroups, name='portgroups'),
    url(r'virtmachines/', views.virtmachines, name='virtmachines'),
]
