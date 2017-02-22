from django.conf.urls import url

from Notissu import views

urlpatterns = [
    url(r'^list/(?P<category>[a-z]+)/(?P<page>\d+)/$', views.get_list, name='list'),
    url(r'^view/(?P<notice_id>\d+)/$', views.get_view, name='view'),
    url(r'^keyword/$', views.keyword, name='keyword'),
    url(r'^keyword/(?P<keyword>.+)/$', views.delete_keyword, name='keyword_view'),
    url(r'^token/$', views.set_token, name='token'),
    url(r'^token/(?P<token>.+)/$', views.delete_token, name='token_view'),
]
