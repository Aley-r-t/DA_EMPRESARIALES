from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    if request.method == 'POST':
        context = {
            'titulo' : 'Formulario',
            'nombre' : request.POST['nombre'],
            'clave'  : request.POST.get('password', 'N/A'),
            'educacion': request.POST.get('educacion'),
            'idiomas': request.POST.getlist('idiomas'),
            'correo': request.POST['email'],
            'website' : request.POST.get('sitioweb', 'N/A'),
        }
        return render(request, 'encuesta/respuesta.html', context)
    else:
        context = {
            'titulo' : 'Formulario',
        }
        return render(request, 'encuesta/index.html')

def enviar(request):
    return render(request, 'encuesta/respuesta.html')