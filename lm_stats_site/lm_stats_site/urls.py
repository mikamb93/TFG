"""lm_stats_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from django.contrib import admin
from lmstats import views, admin_views
from django.contrib.auth.views import login, logout
from lmstats.views import register

admin.autodiscover()

urlpatterns = [
    url(r'^usuarios/', include('lmstats.urls')),
    
    url(r'^admin/actualizar/$', admin_views.actualizar),           
    url(r'^admin/', admin.site.urls),
    url(r'^demo/', views.my_view),
#   url(r'^', views.my_view),
    url(r'^crear/', views.crear, name='crear'),
    url(r'^datos/$', views.mostrardatos),
    
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/register/$', register),
    
    url(r'^mis_pronosticos/', views.mispronosticos),
    url(r'^clasificacion/', views.clasificacion),
    
    
]
