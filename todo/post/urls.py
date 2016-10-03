from django.conf.urls import url

from .views import index, finish

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^erase/(?P<pk>\d+)$', finish, name='finish')
]