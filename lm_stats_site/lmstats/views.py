from django.shortcuts import render, render_to_response, RequestContext

# Create your views here.
def my_view(request):
    a = range(1, 10)
    b = 'string'
    c = 33
    contenido = {
        'titulo' : 'Mi primer gran articulo',
        'autor' : 'Carlos Picca',
        'dia' : '19 de Julio de 2013',
        'contenido' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam cursus tempus dui, ut vulputate nisl eleifend eget. Aenean justo felis, dapibus quis vulputate at, porta et dolor. Praesent enim libero, malesuada nec vestibulum vitae, fermentum nec ligula. Etiam eget convallis turpis. Donec non sem justo.',
    }
    
    
    return render_to_response('index.html', contenido)
