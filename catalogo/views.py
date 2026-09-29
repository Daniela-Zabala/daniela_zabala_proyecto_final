from django.shortcuts import render, redirect
from .forms import ProductoForm

# Create your views here.
#vista de la página de inicio 
def inicio(request):
    return render(request, 'inicio.html')

#vista de Catálogo
def catalogo(request):
    return render(request, 'catalogo.html')

#vista de la pagina de contacto
def contacto(request):
    return render(request, 'contacto.html')

# Vista para crear un nuevo producto
def crear_producto(request):

    if request.method == 'POST':
        form = ProductoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('catalogo')

    else:
        form = ProductoForm()

    return render(
        request,
        'formulario.html',
        {
            'form': form,
            'titulo_formulario': '📦 Añadir nuevo producto',
        }
    )
