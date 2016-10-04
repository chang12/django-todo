from django.conf.urls import url

from .views import index, finish, modify

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^erase/(?P<pk>\d+)$', finish, name='finish'),
    url(r'^modify/(?P<command>.+)$', modify, name='modify'),
]