'''
Created on 26 mar. 2017

@author: mikamb93
'''
import requests

from betEtsii import clasificador
from betEtsii import views_utils
from betEtsii.models import Partido, Apuesta, AuthUser
import datetime as dt


def alimentarPartidosBBDD():
    if(Partido.objects.count()==0):
        rfc = clasificador.seleccionaMejorRFC(20)
        for jornada in range(1,39):
            partidosJorn = partidosJornada(jornada)
            for partido in partidosJorn:
                if (jornada in [1, 2, 3, 4, 5]):
                    detallespartido=detallesPartido(str(partido['id']))
                    porc1 = detallespartido['forecast']['1']
                    porcX = detallespartido['forecast']['X']
                    porc2 = detallespartido['forecast']['2']
                    diferencia = 100 - (int(porc1)+int(porcX)+int(porc2))
                    porcXnuevo = int(porcX) + diferencia
                    porcPartido = [str(porc1), str(porcXnuevo),str(porc2)]
                else:
                    
                    estadisticasConRes = views_utils.statsPartido(partido['id'], partido['year'])
                    estadisticasSinRes = estadisticasConRes[:len(estadisticasConRes) - 1]
                    probabilidades = rfc.predict_proba(estadisticasSinRes)
                    porcPartido = [probabilidades[0][0] * 100, probabilidades[0][2] * 100, probabilidades[0][1] * 100]
                fecha=partido['date']
                fechaFormateada = fecha.replace('/','-')
                jornadaActual = int(partido['round'])
                p = Partido(idpartido=partido['id'], jornada=jornadaActual, fechapartido=fechaFormateada,
                            horapartido=dt.time(int(partido['hour']),int(partido['minute'])),equipo1=partido['local'],
                            equipo2=partido['visitor'],porcentaje1=porcPartido[0],porcentajex=porcPartido[1],
                            porcentaje2=porcPartido[2],competicion=partido['competition_name'],resultado=None,resultadoreal=None)
                p.save()
                
def partidosJornada(jornada):
    urlPartidosJornada = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=matchs&key=4b45eb362a5e4edcf7f75e5ce015a0ea&league=1&round='+str(jornada)+'&order=twin&twolegged=1&year='
    jsondataJornada = requests.get(urlPartidosJornada).json()
    partidos=jsondataJornada['match']
    return partidos
 
def detallesPartido(idPartido):
    urlPartido = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=match&key=4b45eb362a5e4edcf7f75e5ce015a0ea&id='+idPartido+'&year='
    jsondataPartido = requests.get(urlPartido).json()
    return jsondataPartido

def actualizar(data):
    jornada = int(data['jornada'])
    urlEstadoLiga = 'http://apiclient.resultados-futbol.com/scripts/api/api.php?key=4b45eb362a5e4edcf7f75e5ce015a0ea&tz=Europe/Madrid&format=json&req=league_status&id=1&group=1&year=2017'
    jsondataEstado = requests.get(urlEstadoLiga).json()
    estadoActual = int(jsondataEstado['league']['current_round'])
    partidosBBDD=Partido.objects.filter(jornada=jornada)
    if((len(partidosBBDD)!=0)&(jornada<=estadoActual)):
        urlPartidosJornada = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=matchs&key=4b45eb362a5e4edcf7f75e5ce015a0ea&league=1&round='+str(jornada)+'&order=twin&twolegged=1&year='
        jsondataJornada = requests.get(urlPartidosJornada).json()
        partidos=jsondataJornada['match']
        for partido in partidos:
            if(partido['status'] == 1):
                partidoBBDD=Partido.objects.get(idpartido=int(partido['id']))
                partidoBBDD.resultadoreal=partido['result']
                if(partido['local_goals'] > partido['visitor_goals'] ):
                    partidoBBDD.resultado='1'
                elif(partido['local_goals'] < partido['visitor_goals'] ):
                    partidoBBDD.resultado='2'
                else:
                    partidoBBDD.resultado='X'
                partidoBBDD.save()
                apuestasPartido = Apuesta.objects.filter(partido_idpartido=int(partido['id']))
                if (len(apuestasPartido) != 0):
                    for apuesta in apuestasPartido:
                        if(apuesta.pronostico == partidoBBDD.resultado):
                            apuesta.acierto_fallo = 1
                            apuesta.save()
    usuarios = AuthUser.objects.all()
    for usuario in usuarios:
        puntosUsuario = len(Apuesta.objects.filter(usuario_idusuario=usuario).filter(acierto_fallo=True))
        usuario.puntos = puntosUsuario
        usuario.save()

