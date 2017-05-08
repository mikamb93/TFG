from django.contrib.auth import login as auth_login, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import deprecate_current_app
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response, RequestContext, \
    resolve_url
from django.template.context_processors import csrf
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, \
    requires_csrf_token
from django.views.decorators.debug import sensitive_post_parameters

from betEtsii import views_utils
from betEtsii.forms import UsuarioForm, MyRegistrationForm
from betEtsii.models import AuthUser, Usuario, Apuesta, Partido
from betEtsii_site import settings
import datetime as dt
import time as timeModule


# import datetime
# Create your views here.
# @ensure_csrf_cookie
def listarPartidos(request):
    datos, jornada = views_utils.listarPartidos()
    return render(request,'partidos.html', RequestContext(request,{'datos' : datos, 'jornada' : jornada}))

def crear(request):
    if request.POST:
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/')
    else:
        form = UsuarioForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('crear_usuario.html', args)

# @ensure_csrf_cookie
def register(request):
    form = UserCreationForm(data=request.POST or None)
    if request.method == 'POST' :
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('base.html')
        else:
            errores = form.error_messages
            for error in errores :
                print('errores :',error)
    return render(request, 'registration/register.html', {'form': form})

def register_user1(request):
    return render(request, 'registration/register.html')

def register_user(request):
    form = MyRegistrationForm(request.POST)     # create form object
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request, 'registration/register.html', {'registerOK': True})
        else:
            errores = form.error_messages
            for error in errores :
                print('errores :',error)
    
#     args['form'] = MyRegistrationForm()
    return render(request, 'registration/register.html', {'form': form,'registerOK':False})

@deprecate_current_app
@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='mis_pronosticos.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)

# # @csrf_protect
# def login(request, authentication_form=AuthenticationForm):
# 
#     if request.method == "POST":
#         form = authentication_form(request, data=request.POST)
#         if form.is_valid():
# 
# #             # Ensure the user-originating redirection url is safe.
# #             if not is_safe_url(url=redirect_to, host=request.get_host()):
# #                 redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
# 
#             # Okay, security check complete. Log the user in.
#             auth_login(request, form.get_user())
# 
#             return HttpResponseRedirect('/clasificacion')
#     else:
#         form = authentication_form(request)
# 
#     current_site = get_current_site(request)
# 
#     context = {
#         'form': form,
#         'site': current_site,
#         'site_name': current_site.name,
#     }
# 
#     return TemplateResponse(request, 'registration/login.html', context)
    
def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

# @ensure_csrf_cookie
def mispronosticos(request):
    iduser=request.user.username
    apuestasUser = []
    mispuntos = 0
    if not iduser == '':
        iduser = AuthUser.objects.get(username=request.user).idusuario
        if request.POST :
            form = request.POST
            for partido,pron in form.items():
                if(partido == 'csrfmiddlewaretoken'):
                    continue
                try:
                    apuestaYaRealizada = Apuesta.objects.get(usuario_idusuario=iduser, partido_idpartido=partido)
                except Apuesta.DoesNotExist:
                    apuestaYaRealizada = None
                fechaPartido = Partido.objects.get(idpartido=partido).fechapartido
                horaPartido = Partido.objects.get(idpartido=partido).horapartido
                fechaActual = dt.datetime.strptime(timeModule.strftime("%Y-%m-%d"), "%Y-%m-%d").date()
                horaActual = dt.datetime.strptime(timeModule.strftime("%H:%M:%S"), "%H:%M:%S").time()
                datetimeActual = dt.datetime.combine(fechaActual, horaActual)
                datetimePartido = dt.datetime.combine(fechaPartido, horaPartido)
                if not apuestaYaRealizada:
                    if datetimeActual < datetimePartido:
                        authuser = AuthUser.objects.get(username=request.user)
                        part= Partido.objects.get(idpartido=partido)
                        ap=Apuesta(idapuesta=None,usuario_idusuario=authuser,partido_idpartido=part,pronostico=pron,acierto_fallo=False)
                        ap.save()
        apuestasUser = Apuesta.objects.filter(usuario_idusuario=iduser).order_by('-partido_idpartido')
        mispuntos = AuthUser.objects.get(username=request.user).puntos
    return render(request,'mis_pronosticos.html', RequestContext(request,{'pronosticos':apuestasUser,'mispuntos':mispuntos}))
    
def clasificacion(request):
    usuarios = AuthUser.objects.all().order_by('-puntos')
    clasificacionUsuarios = []
    for usuario in usuarios:
        nick = usuario.username
        puntos = usuario.puntos
        apuestasRealizadas = len(Apuesta.objects.filter(usuario_idusuario=usuario.idusuario))
        porcentajeAcierto = 0
        if(apuestasRealizadas != 0):
            porcentajeAcierto = puntos / apuestasRealizadas
        clasificacionUsuarios.append([nick,"%0.2f" % (porcentajeAcierto*100.0)+' %',puntos])
        
    return render(request,'clasificacion.html', RequestContext(request,{'usuarios':clasificacionUsuarios,}))


