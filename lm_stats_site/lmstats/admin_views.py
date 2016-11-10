'''
Created on 8 nov. 2016

@author: mikamb93
'''

from lmstats.models import Partido, Apuesta
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
import requests
 
 
def actualizar(request):
    data=request.POST
    jornada = int(data['jornada'])
    urlEstadoLiga = 'http://apiclient.resultados-futbol.com/scripts/api/api.php?key=27ddfff57083be19645416c230634b71&tz=Europe/Madrid&format=json&req=league_status&id=1&group=1&year=2017'
    jsondataEstado = requests.get(urlEstadoLiga).json()
    estadoActual = int(jsondataEstado['league']['current_round'])
    print(Partido.objects.get(idpartido=96233).resultado)
    partidosBBDD=Partido.objects.filter(jornada=jornada).filter(resultado__isnull=True)
    print(len(partidosBBDD))
    print(jornada<=estadoActual)
    if((len(partidosBBDD)!=0)&(jornada<=estadoActual)):
        print('entra')
        urlPartidosJornada = 'http://www.resultados-futbol.com/scripts/api/api.php?tz=Europe/Madrid&format=json&req=matchs&key=27ddfff57083be19645416c230634b71&league=1&round='+str(jornada)+'&order=twin&twolegged=1&year='
        jsondataJornada = requests.get(urlPartidosJornada).json()
        partidos=jsondataJornada['match']
        for partido in partidos:
            partidoBBDD=Partido.objects.get(idpartido=int(partido['id']))
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
        
    return render_to_response(
        "admin/index.html",
        {},
        RequestContext(request, {}),
    )
report = staff_member_required(actualizar)