'''
Created on 8 nov. 2016

@author: mikamb93
'''

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from betEtsii import admin_views_utils



def alimentarPartidosBBDD(request):
    admin_views_utils.alimentarPartidosBBDD()
    return render_to_response("admin/index.html", 
                              {}, RequestContext(request, {}),)

def actualizar(request):
    data=request.POST
    admin_views_utils.actualizar(data)
    return render_to_response("admin/index.html", 
                              {}, RequestContext(request, {}),)
    
report = staff_member_required(actualizar)