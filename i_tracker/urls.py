from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),

	url(r'^$', views.home, name='home'),
	url(r'^table/$', views.home_table, name='home_table'),
	url(r'^issue/$', views.issue, name='issue'), #new issue
	url(r'^issue/(?P<issue_pk>\d+)/$', views.issue, name='issue'), #issue
	url(r'^issue/delete/(?P<issue_pk>\d+)/$', views.delete_issue, name="delete_issue"), #delete issue

	url(r'^issue/(?P<issue_pk>\d+)/comment/$', views.comment, name='comment'), #new comment for an issue
	url(r'^issue/(?P<issue_pk>\d+)/comment/delete/(?P<comment_pk>\d+)/$', views.delete_comment, name='delete_comment'), #delete comment

	url(r'^get/users/profile/$', views.get_users_profile, name='get_users_profile'),
]