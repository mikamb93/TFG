from django.shortcuts import render, render_to_response, RequestContext,\
    redirect
from lmstats.forms import UsuarioForm
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from lmstats.models import *
import requests
import urllib, json
import urllib.request
import csv
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier as RFC
import time
from datetime import datetime as dt
import datetime
from lmstats import clasificador
from django.http.response import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect,\
    requires_csrf_token
from django.contrib.auth.models import AnonymousUser
from django.template.defaultfilters import default





# Create your views here.
@ensure_csrf_cookie
def my_view(request):

    partidosJornada = partidosJornadaActual('1')
    porcentajes = []
    partidos = []
    datos = []
    
#    p = Partido(idpartido=123,fechapartido=datetime.today(),horapartido=datetime.time(datetime.now()),equipo1='Betis',equipo2='Celta',porcentaje1=50,porcentajex=20,porcentaje2=30,competicion='Liga',resultado=None)
#    p.save()
    for partido in partidosJornada:
        if (len(Partido.objects.filter(idpartido=int(partido['id']))) == 0):
            
            detallespartido=detallesPartido(str(partido['id']))
            if (int(partido['round']) in [1, 2, 3, 4, 5]):
                porc1 = detallespartido['forecast']['1']
                porcX = detallespartido['forecast']['X']
                porc2 = detallespartido['forecast']['2']
                diferencia = 100 - (int(porc1)+int(porcX)+int(porc2))
                porcXnuevo = int(porcX) + diferencia
                porcPartido = [str(porc1), str(porcXnuevo),str(porc2)]
                porcentajes.append(porcPartido)
            else:
                rfc = clasificador.seleccionaMejorRFC(10)
                estadisticasConRes = statsPartido(partido['id'], partido['year'])
                estadisticasSinRes = estadisticasConRes[:len(estadisticasConRes) - 1]
                probabilidades = rfc.predict_proba(estadisticasSinRes)
                porcPartido = [probabilidades[0][0] * 100, probabilidades[0][2] * 100, probabilidades[0][1] * 100]
                porcentajes.append(porcPartido)
            fecha=partido['date']
            fechaFormateada = fecha.replace('/','-')
            jornadaActual = int(partido['round'])
            p = Partido(idpartido=partido['id'], jornada=jornadaActual, fechapartido=fechaFormateada,
                        horapartido=datetime.time(int(partido['hour']),int(partido['minute'])),equipo1=partido['local'],
                        equipo2=partido['visitor'],porcentaje1=porcPartido[0],porcentajex=porcPartido[1],
                        porcentaje2=porcPartido[2],competicion=partido['competition_name'],resultado=None)
            p.save()
        else:
            p = Partido.objects.get(idpartido=partido['id'])
            
#        partidoToString = partido['local']+' - '+partido['visitor']
        partidoToString = p.__str__()
        partidos.append(partidoToString)
        porcentaje1=int(p.porcentaje1)
        porcentajeX=int(p.porcentajex)
        porcentaje2=int(p.porcentaje2)
        if(porcentaje1 >= porcentajeX and porcentaje1 >= porcentaje2):
            pronosticoRecomendado="Gana "+p.equipo1
        elif(porcentajeX >= porcentaje1 and porcentajeX >= porcentaje2):
            pronosticoRecomendado="Empate"
        elif(porcentaje2 >= porcentaje1 and porcentaje2 >= porcentajeX):
            pronosticoRecomendado="Gana "+p.equipo2
        
        listaPorcentajes=[porcentaje1,porcentajeX,porcentaje2]
        fechaPartido=datetime.datetime.strptime(str(p.fechapartido),'%Y-%m-%d').strftime('%d/%m/%Y')
        horaPartido=datetime.datetime.strptime(str(p.horapartido),'%H:%M:%S').strftime('%H:%M')
        id=p.idpartido
        
        datos.append([partidoToString,listaPorcentajes,fechaPartido,horaPartido,pronosticoRecomendado,id])
    
    return render_to_response('base.html',{'datos' : datos})


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


def usuarios(request):
    return render_to_response('index.html', {'usuarios' : AuthUser.objects.all() })

def usuario(request, usuario_id=1):
    return render_to_response('usuario.html', {'usuario' : Usuario.objects.get(idusuario=usuario_id) })


def mostrardatos(request):
#     r = requests.get('http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=tables&key=27ddfff57083be19645416c230634b71&league=1&group=1&year=2016&round=30')
#     jsonData = r.content
#     jsonToPython = json.loads()
#     print (r.content)
    
    url = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=tables&key=27ddfff57083be19645416c230634b71&league=1&group=1&year=2016&round=30'
#     jsondata = requests.get(url).json()
#     for equipo in jsondata['table']:
#         if equipo['team'] == 'Barcelona':
#             print (equipo['team_abbr'])
#             break
#     print (jsondata['table'][0])
#     print(datosEquipo('2080', '31', '1', '2016'))
#     print(enfrentamientosDirectos('184216','2107','%20369','2014'))
#     statsRMEibar=statsPartido('19959', '2015')
#     c = csv.writer(open("datosLiga1.csv","a"))
# #    c.writerow(['Posicion Local','%V Local','%E Local','%D Local','GF Local','GC Local','Forma Local','Enfr Directos Local','Enfr Directos Empates','Enfr Directos Visitante','Posicion Visitante','%V Visitante','%E Visitante','%D Visitante','GF Visitante','GC Visitante','Forma Visitante','Resultado'])
#     c.writerow(['___________________________________________2016_______________________________________________'])
#     generaFilasTemporada('1', '2016', c)
#    generaDataSetLiga('1', '2008')
    return render_to_response('datos.html', {'datos' : None})


def formaEquipo(forma):
    victorias=forma.count('w')
    empates=forma.count('d')
    return victorias*3 + empates


def datosEquipo(idEquipo,jornada,liga,ano):
    jornadaParaAnalisis=str(int(jornada)-1) #Los datos para el analisis tienen que ser los reales justo antes del partido
    url = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=tables&key=27ddfff57083be19645416c230634b71&league='+liga+'&round='+jornadaParaAnalisis+'&year='+ano
    jsondata = requests.get(url).json()
    for equipo in jsondata['table']:
        if equipo['id']==idEquipo:
            pos=int(equipo['pos'])
            porcentV = int(round(int(equipo['wins'])/int(equipo['round'])*100,0))
            porcentE = int(round(int(equipo['draws'])/int(equipo['round'])*100,0))
            porcentD = int(round(int(equipo['losses'])/int(equipo['round'])*100,0))
            golesF = int(equipo['gf'])
            golesC = int(equipo['ga'])
#            forma = formaEquipo(equipo['form'])
            datos=[pos,porcentV,porcentE,porcentD,golesF,golesC] #Anadir aqui la forma
            break
    return datos

def enfrentamientosDirectos(idPartido,idEquipo1,idEquipo2,ano):
    url = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&lang=es&format=json&req=teams_history&key=27ddfff57083be19645416c230634b71&id='+idPartido+'&year='+ano+'&teams='+idEquipo1+','+idEquipo2
    jsondata = requests.get(url).json()
    if (jsondata['matches'] is not None):
        ultimos5 = jsondata['matches'][0:5]
    else:
        return [0,0,0]
    
    urlEq1 = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=team&key=27ddfff57083be19645416c230634b71&id='+idEquipo1
    urlEq2 = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=team&key=27ddfff57083be19645416c230634b71&id='+idEquipo2
    jsondataEq1 = requests.get(urlEq1).json()
    jsondataEq2 = requests.get(urlEq2).json()
    equipo1=jsondataEq1['team']['nameShow']
    equipo2=jsondataEq2['team']['nameShow']
    
    victEquipo1=0
    empates=0
    victEquipo2=0
    for partido in ultimos5:
        if partido['local_goals'] == partido['visitor_goals']:
            empates+=1
        elif (partido['local_goals'] > partido['visitor_goals']) & (partido['local'] == equipo1):
            victEquipo1+=1
        elif (partido['local_goals'] > partido['visitor_goals']) & (partido['local'] == equipo2):
            victEquipo2+=1
        elif (partido['local_goals'] < partido['visitor_goals']) & (partido['local'] == equipo1):
            victEquipo2+=1
        elif (partido['local_goals'] < partido['visitor_goals']) & (partido['local'] == equipo2):
            victEquipo1+=1
    return [victEquipo1,empates,victEquipo2]


def statsPartido(idPartido,ano):
    url = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=match&key=27ddfff57083be19645416c230634b71&id='+idPartido+'&year='+ano
    partido = requests.get(url).json()
    idEquipo1 = partido['datateam1']
    idEquipo2 = partido['datateam2']
    jornada = partido['round']
    if(partido['league'] == 'Primera Divisi\u00f3n'):
        liga='1'
    datosEquipo1=datosEquipo(idEquipo1, jornada, liga, ano)
    datosEquipo2=datosEquipo(idEquipo2, jornada, liga, ano)
#    enfrentamientos = enfrentamientosDirectos(idPartido, idEquipo1, idEquipo2, ano)
    if(partido['local_goals'] > partido['visitor_goals'] ):
        resultado = 1
    elif(partido['local_goals'] < partido['visitor_goals'] ):
        resultado = 2
    else:
        resultado = 3
    estadisticas=datosEquipo1 + datosEquipo2 # Agregar aqui '+ enfrentamientos'
    estadisticas.append(resultado)
    return estadisticas


def generaFilasTemporada(liga,ano,c):
    urlultimajornada = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=matchs&key=27ddfff57083be19645416c230634b71&league='+liga+'&round=&order=twin&twolegged=1&year='+ano
    jsondataultimajornada = requests.get(urlultimajornada).json()
    numJornadas = int(jsondataultimajornada['match'][0]['round'])
#    matrizPartidos = []
    i=0
#    c.writerow(['Posicion Local','%V Local','%E Local','%D Local','GF Local','GC Local','Forma Local','Enfr Directos Local','Enfr Directos Empates','Enfr Directos Visitante','Posicion Visitante','%V Visitante','%E Visitante','%D Visitante','GF Visitante','GC Visitante','Forma Visitante','Resultado'])
    for jornada in range(6,numJornadas+1): #Necesitamos tener todas las filas con 5 partidos de forma actual
        urlPartidosJornada = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=matchs&key=27ddfff57083be19645416c230634b71&league='+liga+'&round='+str(jornada)+'&order=twin&twolegged=1&year='+ano
        jsondataJornada = requests.get(urlPartidosJornada).json()
        for partido in jsondataJornada['match']:
            estadisticasPartido=statsPartido(partido['id'], partido['year'])
#            matrizPartidos.append(estadisticasPartido)
            c.writerow(estadisticasPartido)
            i+=1
            print(i)
#    return matrizPartidos

def generaDataSetLiga(liga, anoComienzo):
    c = csv.writer(open("datosLiga"+liga+".csv","w"))
    c.writerow(['Posicion Local','%V Local','%E Local','%D Local','GF Local','GC Local','Forma Local','Enfr Directos Local','Enfr Directos Empates','Enfr Directos Visitante','Posicion Visitante','%V Visitante','%E Visitante','%D Visitante','GF Visitante','GC Visitante','Forma Visitante','Resultado'])
    anoActual = dt.now().year
    for ano in range(int(anoComienzo), anoActual+1):
        if (ano == 2013 or ano == 2014):
            continue
        else:
            print("Ano : ____________________________________________________"+str(ano))
            generaFilasTemporada(liga, str(ano),c)
    
def partidosJornadaActual(liga):
    urlJornadaActual='http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=league_status&key=27ddfff57083be19645416c230634b71&id=1&group=1&year=2017'
    jsondataJornadaActual = requests.get(urlJornadaActual).json()
    jornadaActual = str(int(jsondataJornadaActual['league']['current_round']))
    urlPartidosJornada = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=matchs&key=27ddfff57083be19645416c230634b71&league='+liga+'&round='+jornadaActual+'&order=twin&twolegged=1&year='
    jsondataJornada = requests.get(urlPartidosJornada).json()
    partidos=jsondataJornada['match']
    return partidos

def detallesPartido(idPartido):
    urlPartido = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=match&key=27ddfff57083be19645416c230634b71&id='+idPartido+'&year='
    jsondataPartido = requests.get(urlPartido).json()
    return jsondataPartido


 

@ensure_csrf_cookie
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

@csrf_protect
def login(request):
 
    # If we submitted the form...
    if request.method == 'POST':
 
        # Check that the test cookie worked (we set it below):
        if request.session.test_cookie_worked():
 
            # The test cookie worked, so delete it.
            request.session.delete_test_cookie()
 
            # In practice, we'd need some logic to check username/password
            # here, but since this is an example...
            return HttpResponse("You're logged in.")
 
        # The test cookie failed, so display an error message. If this
        # was a real site we'd want to display a friendlier message.
        else:
            return HttpResponse("Please enable cookies and try again.")
  
    # If we didn't post, send the test cookie along with the login form.
    request.session.set_test_cookie()
    return render(request,'foo/login_form.html')
    
def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

@ensure_csrf_cookie
def mispronosticos(request):
    
    if request.user is not AnonymousUser:
        iduser = AuthUser.objects.get(username=request.user).idusuario
        if request.POST :
            form = request.POST
            
            for partido,pron in form.items():
                if not Apuesta.objects.filter(usuario_idusuario=iduser, partido_idpartido=partido):
                    authuser = AuthUser.objects.get(username=request.user)
                    part= Partido.objects.get(idpartido=partido)
                    ap=Apuesta(idapuesta=None,usuario_idusuario=authuser,partido_idpartido=part,pronostico=pron,acierto_fallo=False)
                    ap.save()
    
        apuestasUser = Apuesta.objects.filter(usuario_idusuario=iduser)    
        
    
    
    return render(request,'mis_pronosticos.html', RequestContext(request,{'pronostico':apuestasUser,}))
    
    
#     if request.method == "POST":
#         
#         pronostico = request.post_data
#         return redirect('success.html')
#     else:
#         
#         return render(request, 'mis_pronosticos.html', RequestContext(request, {'pronostico':pronostico,  }))  


def clasificacion(request):
    apuestasAcertadas = Apuesta.objects.filter(acierto_fallo=1)
    if(len(apuestasAcertadas)>0):
        dictUsuarios={}
        listaUsuariosRegistrados=AuthUser.objects.all()
        for usuario in listaUsuariosRegistrados:
            dictUsuarios[usuario.idusuario]=0
        for apuesta in apuestasAcertadas:
            dictUsuarios[apuesta.usuario_idusuario.idusuario] = dictUsuarios[apuesta.usuario_idusuario.idusuario]+1
        items = dictUsuarios.items()
        items.sort(key=lambda x: x[1])
        print(items)
        
    return render(request,'clasificacion.html', RequestContext(request,{'usuarios':items,}))


