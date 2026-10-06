from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required

from .forms import ProductoForm, RegistroUsuarioForm
from .models import Producto, Reserva


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
@permission_required(
    'catalogo.add_producto',
    raise_exception=True
)  #limitar al adm para que solo ese usuario pueda crear prod
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


# Vista para editar un producto
@permission_required(
    'catalogo.change_producto',
    raise_exception=True
)  #limitar al adm para que solo ese usuario pueda editar prod
def editar_producto(request, producto_id):

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    if request.method == 'POST':
        form = ProductoForm(
            request.POST,
            instance=producto
        )

        if form.is_valid():
            form.save()
            return redirect('catalogo')

    else:
        form = ProductoForm(
            instance=producto
        )

    return render(
        request,
        'formulario.html',
        {
            'form': form,
            'titulo_formulario': '✏️ Editar producto',
        }
    )


# Vista para eliminar un producto
@permission_required(
    'catalogo.delete_producto',
    raise_exception=True
)  #limitar al adm para que solo ese usuario pueda eliminar prod
def eliminar_producto(request, producto_id):

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    if request.method == 'POST':
        producto.delete()
        return redirect('catalogo')

    return render(
        request,
        'confirmar_eliminar.html',
        {
            'producto': producto
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


#Vista para iniciar sesión
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


#Vista para consultar las reservas del usuario
def mis_reservas(request):

    if request.user.is_authenticated:

        reservas = Reserva.objects.filter(
            usuario=request.user
        )

        return render(
            request,
            'mis_reservas.html',
            {
                'reservas': reservas
            }
        )

    return redirect('login')