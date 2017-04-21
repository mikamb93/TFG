
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout

from betEtsii import views, admin_views
from betEtsii.views import register, register_user, register_user1
from betEtsii_site import settings


admin.autodiscover()

urlpatterns = [

    
    url(r'^media/$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^usuarios/', include('betEtsii.urls')),
    url(r'^admin/alimentar/$', admin_views.alimentarPartidosBBDD),
    url(r'^admin/actualizar/$', admin_views.actualizar),           
    url(r'^admin/', admin.site.urls),
    url(r'^partidos/', views.listarPartidos),
    url(r'^crear/', views.crear, name='crear'),
    
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout, {'next_page': '/partidos/'}),
    url(r'^accounts/register1/$', register_user1),
    url(r'^accounts/register2/$', register_user),
    
    url(r'^mis_pronosticos/', views.mispronosticos),
    url(r'^clasificacion/', views.clasificacion),
    
    
]
