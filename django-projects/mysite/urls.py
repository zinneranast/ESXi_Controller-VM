from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^CS/', include('CS.urls')),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^', include('CS.urls')),
]
