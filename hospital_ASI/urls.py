from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    url(r'^', include('i_tracker.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
