'''
Created on 15 jul. 2016

@author: mikamb93
'''

from django.conf.urls import url
from lmstats import views

urlpatterns = [
    url(r'^todos/$', views.usuarios),
    url(r'^obtener/(?P<usuario_id>\d+)/$', views.usuario),
    url(r'^datos/$', views.mostrardatos),
    
]