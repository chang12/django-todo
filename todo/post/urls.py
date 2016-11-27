from django.conf.urls import url

from .views import backlog
from .views import delete
from .views import finish
from .views import hold_off
from .views import index
from .views import label_create
from .views import label_delete
from .views import labeling
from .views import modify
from .views import move
from .views import start

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^backlog$', backlog, name='backlog'),

    url(r'^erase/(?P<pk>\d+)$', finish, name='finish'),
    url(r'^move/(?P<command>.+)$', move, name='move'),
    url(r'^modify/(?P<pk>\d+)$', modify, name='modify'),
    url(r'^hold_off/(?P<pk>\d+)$', hold_off, name='hold_off'),
    url(r'^delete/(?P<pk>\d+)$', delete, name='delete'),
    url(r'^start/(?P<pk>\d+)$', start, name='start'),

    url(r'^labels$', label_create, name='label_create'),
    url(r'^labeling$', labeling, name='labeling'),
    url(r'^label_delete', label_delete, name='label_delete'),
]