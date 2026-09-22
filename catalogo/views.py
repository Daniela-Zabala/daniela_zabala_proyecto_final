from django.shortcuts import render

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def catalogo(request):
    return render(request, 'catalogo.html')

def contacto(request):
    return render(request, 'contacto.html')
