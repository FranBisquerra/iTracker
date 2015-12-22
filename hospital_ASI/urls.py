from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    url(r'^iTracker/', include('i_tracker.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
