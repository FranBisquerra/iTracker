from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^home/$', views.home, name='home'),
	url(r'^home/table/$', views.home_table, name='home_table'),
	url(r'^home/issue/$', views.issue, name='issue'), #new issue
	url(r'^home/issue/(?P<issue_pk>\d+)/$', views.issue, name='issue'), #issue
	url(r'^home/issue/delete/(?P<issue_pk>\d+)/$', views.delete_issue, name="delete_issue"), #delete issue

	url(r'^home/issue/(?P<issue_pk>\d+)/comment$', views.comment, name='comment'), #new comment for an issue
	url(r'^home/issue/(?P<issue_pk>\d+)/comment/(?P<comment_pk>\d+)/$', views.comment, name='comment'), #comment
	url(r'^home/issue/(?P<issue_pk>\d+)/comment/delete/(?P<comment_pk>\d+)/$', views.delete_comment, name='delete_comment'), #delete comment
]