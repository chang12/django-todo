from django.conf.urls import url

from .views import index, erase

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^erase/(?P<pk>\d+)$', erase, name='erase')
]