from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'service_list/', views.service_list, name='service_list'),
    url(r'connect/', views.connect, name='connect'),
    url(r'login/', views.login, name='login'),
]
