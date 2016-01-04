from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^home/$', views.home, name='home'),
	url(r'^home/table/$', views.home_table, name='home_table'),
	url(r'^home/issue/$', views.issue, name='issue'), #new issue
	url(r'^home/issue/(?P<issue_pk>\d+)/$', views.issue, name='issue'), #issue
]