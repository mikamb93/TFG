
from django.conf.urls import url, include

from django.contrib import admin
from lmstats import views, admin_views
from django.contrib.auth.views import login, logout
from lmstats.views import register
from lm_stats_site import settings


admin.autodiscover()

urlpatterns = [

    
    url(r'^media/$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^usuarios/', include('lmstats.urls')),
    
    url(r'^admin/actualizar/$', admin_views.actualizar),           
    url(r'^admin/', admin.site.urls),
    url(r'^partidos/', views.my_view),
#   url(r'^', views.my_view),
    url(r'^crear/', views.crear, name='crear'),
    url(r'^datos/$', views.mostrardatos),
    
    url(r'^accounts/login/$',  views.login),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/register/$', register),
    
    url(r'^mis_pronosticos/', views.mispronosticos),
    url(r'^clasificacion/', views.clasificacion),
    
    
]
