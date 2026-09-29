from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .forms import ProductoForm, RegistroUsuarioForm
from .models import Producto


# Vista de la página de inicio
def inicio(request):
    return render(request, 'inicio.html')


# Vista del catálogo
def catalogo(request):
    productos = Producto.objects.all()

    return render(
        request,
        'catalogo.html',
        {
            'productos': productos
        }
    )


# Vista de la página de contacto
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


# Vista para registrar un nuevo usuario
def registro(request):

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save()

            login(request, usuario)

            return redirect('inicio')

    else:
        form = RegistroUsuarioForm()

    return render(
        request,
        'registro/registro.html',
        {
            'form': form
        }
    )


# Vista para iniciar sesión
def iniciar_sesion(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            login(request, usuario)
            return redirect('inicio')

        else:
            return render(
                request,
                'registro/login.html',
                {
                    'error': 'El usuario o la contraseña no son correctos.'
                }
            )

    return render(request, 'registro/login.html')