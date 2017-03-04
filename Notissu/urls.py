from django.conf.urls import url

from Notissu import views

urlpatterns = [
    url(r'^list/(?P<category>[a-z]+)/(?P<page>\d+)/$', views.get_list, name='list'),
    url(r'^search/(?P<keyword>.+)/(?P<page>\d+)/$', views.search_list, name='search_list'),
    url(r'^view/(?P<notice_id>\d+)/$', views.get_view, name='view'),
    url(r'^keyword/(?P<token>.+)/(?P<keyword>.+)/$', views.delete_keyword, name='keyword_view'),
    url(r'^keyword/(?P<token>.+)/$', views.keyword, name='keyword'),
    url(r'^token/(?P<token>.+)/$', views.delete_token, name='token_view'),
    url(r'^token/$', views.set_token, name='token'),

]
