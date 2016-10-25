from django.conf.urls import url

from .views import index, finish, move, modify, hold_off, delete

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^erase/(?P<pk>\d+)$', finish, name='finish'),
    url(r'^move/(?P<command>.+)$', move, name='move'),
    url(r'^modify/(?P<pk>\d+)$', modify, name='modify'),
    url(r'^hold_off/(?P<pk>\d+)$', hold_off, name='hold_off'),
    url(r'^delete/(?P<pk>\d+)$', delete, name='delete'),
]