from django.conf.urls import url

from Notissu import views

urlpatterns = [
    url(r'^list/(?P<category>[a-z]+)/(?P<page>\d+)/$', views.get_list, name='list'),
    url(r'^view/(?P<notice_id>\d+)/$', views.get_view, name='view'),
]
