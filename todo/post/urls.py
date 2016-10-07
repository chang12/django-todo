from django.conf.urls import url

from .views import index, finish, move, modify

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^erase/(?P<pk>\d+)$', finish, name='finish'),
    url(r'^move/(?P<command>.+)$', move, name='move'),
    url(r'^modify/(?P<pk>\d+)$', modify, name='modify'),
]