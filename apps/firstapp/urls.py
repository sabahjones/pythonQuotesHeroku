from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^register$', register),
    url(r'^login$', login),
    url(r'^quotes$', quotes),
    url(r'^addquote$', addquote),
    url(r'^addfave/(?P<id>\d+)$', addfave),
    url(r'^deletefave/(?P<id>\d+)$', deletefave),
    url(r'^showuser/(?P<id>\d+)$', showuser),
    url(r'^deletequote/(?P<id>\d+)$', deletequote),
    url(r'^logout$', logout),
]
