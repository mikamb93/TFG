'''
Created on 26 mar. 2017

@author: mikamb93
'''

import csv

import requests

from betEtsii.models import Partido
import datetime as dt
import time as timeModule
from MySQLdb.constants.FIELD_TYPE import NULL


def formaEquipo(forma):
    victorias=forma.count('w')
    empates=forma.count('d')
    return victorias*3 + empates

def listarPartidos():
    partidosJornada, jornadaActual = partidosJornadaActual('1')
    partidos = []
    datos = []
    
    for partido in partidosJornada:
        p = Partido.objects.get(idpartido=partido['id'])
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
        fechaPartido=dt.datetime.strptime(str(p.fechapartido),'%Y-%m-%d').strftime('%d/%m/%Y')
        horaPartido=dt.datetime.strptime(str(p.horapartido),'%H:%M:%S').strftime('%H:%M')
        
        # Comprobar si se puede apostar sobre el partido
        fechaPartidoDate = p.fechapartido
        horaPartidoTime = p.horapartido
        fechaActual = dt.datetime.strptime(timeModule.strftime("%Y-%m-%d"), "%Y-%m-%d").date()
        horaActual = dt.datetime.strptime(timeModule.strftime("%H:%M:%S"), "%H:%M:%S").time()
        datetimeActual = dt.datetime.combine(fechaActual, horaActual)
        datetimePartido = dt.datetime.combine(fechaPartidoDate, horaPartidoTime)
        sePuedeApostar = True
        if datetimeActual > datetimePartido:
            sePuedeApostar = False
        id=p.idpartido
        resultado=p.resultadoreal
        
        datos.append([partidoToString,listaPorcentajes,fechaPartido,horaPartido,pronosticoRecomendado,id,sePuedeApostar,resultado])
    return datos, jornadaActual

def enfrentamientosDirectos(idPartido,idEquipo1,idEquipo2,ano):
    url = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&lang=es&format=json&req=teams_history&key=4b45eb362a5e4edcf7f75e5ce015a0ea&id='+idPartido+'&year='+ano+'&teams='+idEquipo1+','+idEquipo2
    jsondata = requests.get(url).json()
    if (jsondata['matches'] is not None):
        ultimos5 = jsondata['matches'][0:5]
    else:
        return [0,0,0]
    
    urlEq1 = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=team&key=4b45eb362a5e4edcf7f75e5ce015a0ea&id='+idEquipo1
    urlEq2 = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=team&key=4b45eb362a5e4edcf7f75e5ce015a0ea&id='+idEquipo2
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




def generaFilasTemporada(liga,ano,c):
    urlultimajornada = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=matchs&key=4b45eb362a5e4edcf7f75e5ce015a0ea&league='+liga+'&round=&order=twin&twolegged=1&year='+ano
    jsondataultimajornada = requests.get(urlultimajornada).json()
    numJornadas = int(jsondataultimajornada['match'][0]['round'])
#    matrizPartidos = []
    i=0
#    c.writerow(['Posicion Local','%V Local','%E Local','%D Local','GF Local','GC Local','Forma Local','Enfr Directos Local','Enfr Directos Empates','Enfr Directos Visitante','Posicion Visitante','%V Visitante','%E Visitante','%D Visitante','GF Visitante','GC Visitante','Forma Visitante','Resultado'])
    for jornada in range(6,numJornadas+1): #Necesitamos tener todas las filas con 5 partidos de forma actual
        urlPartidosJornada = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=matchs&key=4b45eb362a5e4edcf7f75e5ce015a0ea&league='+liga+'&round='+str(jornada)+'&order=twin&twolegged=1&year='+ano
        jsondataJornada = requests.get(urlPartidosJornada).json()
        for partido in jsondataJornada['match']:
            estadisticasPartido=statsPartido(partido['id'], partido['year'])
#            matrizPartidos.append(estadisticasPartido)
            c.writerow(estadisticasPartido)
            i+=1
#    return matrizPartidos

def statsPartido(idPartido,ano):
    url = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=match&key=4b45eb362a5e4edcf7f75e5ce015a0ea&id='+idPartido+'&year='+ano
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

def datosEquipo(idEquipo,jornada,liga,ano):
    jornadaParaAnalisis=str(int(jornada)-1) #Los datos para el analisis tienen que ser los reales justo antes del partido
    url = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=tables&key=4b45eb362a5e4edcf7f75e5ce015a0ea&league='+liga+'&round='+jornadaParaAnalisis+'&year='+ano
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


def generaDataSetLiga(liga, anoComienzo):
    c = csv.writer(open("datosLiga"+liga+".csv","w"))
    c.writerow(['Posicion Local','%V Local','%E Local','%D Local','GF Local','GC Local','Forma Local','Enfr Directos Local','Enfr Directos Empates','Enfr Directos Visitante','Posicion Visitante','%V Visitante','%E Visitante','%D Visitante','GF Visitante','GC Visitante','Forma Visitante','Resultado'])
    anoActual = dt.datetime.now().year
    for ano in range(int(anoComienzo), anoActual+1):
        if (ano == 2013 or ano == 2014):
            continue
        else:
            generaFilasTemporada(liga, str(ano),c)
    
def partidosJornadaActual(liga):
    urlJornadaActual='http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=league_status&key=4b45eb362a5e4edcf7f75e5ce015a0ea&id=1&group=1&year=2017'
    jsondataJornadaActual = requests.get(urlJornadaActual).json()
    jornadaActual = str(int(jsondataJornadaActual['league']['current_round']))
    urlPartidosJornada = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=matchs&key=4b45eb362a5e4edcf7f75e5ce015a0ea&league='+liga+'&round='+jornadaActual+'&order=twin&twolegged=1&year='
    jsondataJornada = requests.get(urlPartidosJornada).json()
    # Comprobamos que la jornada que se va a mostrar no ha terminado completamente
    if(jsondataJornada['match'][9]['status'] == 1):
        jornadaActual = str(int(jsondataJornadaActual['league']['current_round'])+1)
        urlPartidosJornada = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=matchs&key=4b45eb362a5e4edcf7f75e5ce015a0ea&league='+liga+'&round='+jornadaActual+'&order=twin&twolegged=1&year='
        jsondataJornada = requests.get(urlPartidosJornada).json()
    partidos=jsondataJornada['match']
    return partidos,jornadaActual
