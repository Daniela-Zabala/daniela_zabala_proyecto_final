"""Vistas de TechCovers para gestionar el catálogo y las reservas."""

import logging

from .excepciones import StockInsuficienteError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.db import transaction
from .forms import ProductoForm, RegistroUsuarioForm
from .models import Producto, Reserva, Producto_reserva


#Configuración del logger
logger = logging.getLogger(__name__)


class ValidadorStock:
    """Valida el stock disponible para las reservas."""

    def __init__(self, stock):
        """Guarda el stock en un atributo privado."""
        self.__stock = stock

    def validar(self, cantidad):
        """Comprueba que la cantidad no supere el stock."""
        if cantidad > self.__stock:
            raise StockInsuficienteError(
                "No hay suficientes existencias disponibles."
            )


#Vista de la página de inicio
def inicio(request):
    """Muestra la página principal de TechCovers."""
    return render(request, 'inicio.html')


#Vista del catálogo
def catalogo(request):
    """Muestra los productos disponibles en el catálogo."""
    productos = Producto.objects.all()

    return render(
        request,
        'catalogo.html',
        {
            'productos': productos
        }
    )


#Vista de la página de contacto
def contacto(request):
    """Muestra la página de contacto."""
    return render(request, 'contacto.html')


#Vista para crear un nuevo producto
#limitar al adm para que solo ese usuario pueda crear prod
@permission_required(
    'catalogo.add_producto',
    raise_exception=True
)

  
def crear_producto(request):
    """Permite al administrador crear un producto."""
    if request.method == 'POST':
        form = ProductoForm(request.POST)

        if form.is_valid():
            try:
                producto = form.save()
                logger.info(
                    "Producto creado: %s (ID: %s)",
                    producto.nombre,
                    producto.id
                )
                return redirect('catalogo')

            except Exception:
                logger.exception("Error al crear un producto")
                raise

        logger.warning("Formulario inválido al crear un producto")

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


#Vista para editar un producto
#limitar al adm para que solo ese usuario pueda editar prod
@permission_required(
    'catalogo.change_producto',
    raise_exception=True
)  


def editar_producto(request, producto_id):
    """Permite al administrador modificar un producto existente."""
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
            try:
                producto = form.save()
                logger.info(
                    "Producto modificado: %s (ID: %s)",
                    producto.nombre,
                    producto.id
                )
                return redirect('catalogo')

            except Exception:
                logger.exception(
                    "Error al modificar el producto ID %s",
                    producto_id
                )
                raise

        logger.warning(
            "Formulario inválido al editar el producto ID %s",
            producto_id
        )

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


#Vista para eliminar un producto
#limitar al adm para que solo ese usuario pueda eliminar prod
@permission_required(
    'catalogo.delete_producto',
    raise_exception=True
) 
 

def eliminar_producto(request, producto_id):
    """Permite al administrador eliminar un producto."""
    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    if request.method == 'POST':
        try:
            nombre_producto = producto.nombre
            producto.delete()

            logger.info(
                "Producto eliminado: %s (ID: %s)",
                nombre_producto,
                producto_id
            )
            return redirect('catalogo')

        except Exception:
            logger.exception(
                "Error al eliminar el producto ID %s",
                producto_id
            )
            raise

    return render(
        request,
        'confirmar_eliminacion.html',
        {
            'producto': producto
        }
    )


#Vista para registrar un nuevo usuario
def registro(request):
    """Gestiona el registro de nuevos usuarios."""
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            try:
                usuario = form.save()
                login(request, usuario)

                logger.info(
                    "Nuevo usuario registrado: %s",
                    usuario.username
                )
                return redirect('inicio')

            except Exception:
                logger.exception("Error al registrar un usuario")
                raise

        logger.warning("Formulario inválido durante el registro")

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
    """Autentica al usuario e inicia su sesión."""
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
            logger.info("Inicio de sesión correcto: %s", username)
            return redirect('inicio')

        else:
            logger.warning(
                "Intento de inicio de sesión fallido para: %s",
                username
            )
            return render(
                request,
                'registro/login.html',
                {
                    'error': 'El usuario o la contraseña no son correctos.'
                }
            )

    return render(request, 'registro/login.html')


# Vista para crear una reserva
@login_required
def crear_reserva(request, producto_id):
    """Crea una reserva y actualiza el stock del producto."""
    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('cantidad', 1))

        except (TypeError, ValueError):
            logger.warning(
                "Cantidad inválida al reservar el producto ID %s",
                producto_id
            )
            return render(
                request,
                'crear_reserva.html',
                {
                    'producto': producto,
                    'error': 'La cantidad introducida no es válida.'
                }
            )

        if cantidad <= 0:
            logger.warning(
                "Cantidad no válida (%s) para el producto ID %s",
                cantidad,
                producto_id
            )
            return render(
                request,
                'crear_reserva.html',
                {
                    'producto': producto,
                    'error': 'La cantidad debe ser mayor que 0.'
                }
            )

        #Comprobar el stock mediante una excepción personalizada
        try:
            ValidadorStock(producto.stock).validar(cantidad)

        except StockInsuficienteError as error:
            logger.warning(
                "Stock insuficiente para el producto ID %s: %s",
                producto_id,
                error
            )
            return render(
                request,
                'crear_reserva.html',
                {
                    'producto': producto,
                    'error': str(error)
                }
            )

        try:
            with transaction.atomic():
                reserva = Reserva.objects.create(
                    usuario=request.user,
                    estado='Pendiente'
                )

                Producto_reserva.objects.create(
                    producto=producto,
                    reserva=reserva,
                    cantidad=cantidad
                )

                producto.stock -= cantidad
                producto.save()

            logger.info(
                "Reserva creada: ID %s, usuario %s, producto ID %s, "
                "cantidad %s",
                reserva.id,
                request.user.username,
                producto_id,
                cantidad
            )

            return redirect('mis_reservas')

        except Exception:
            logger.exception(
                "Error al crear una reserva para el producto ID %s",
                producto_id
            )
            raise

    return render(
        request,
        'crear_reserva.html',
        {
            'producto': producto
        }
    )


#Vista para editar una reserva
@login_required
def editar_reserva(request, reserva_id):
    """Modifica la cantidad de productos de una reserva."""
    reserva = get_object_or_404(
        Reserva,
        id=reserva_id,
        usuario=request.user
    )

    producto_reserva = reserva.productos.first()

    if producto_reserva is None:
        logger.warning(
            "La reserva ID %s no contiene productos",
            reserva_id
        )
        return redirect('mis_reservas')

    producto = producto_reserva.producto
    cantidad_actual = producto_reserva.cantidad

    if request.method == 'POST':
        try:
            nueva_cantidad = int(
                request.POST.get('cantidad', cantidad_actual)
            )

        except (TypeError, ValueError):
            logger.warning(
                "Cantidad inválida al editar la reserva ID %s",
                reserva_id
            )
            return render(
                request,
                'editar_reserva.html',
                {
                    'reserva': reserva,
                    'producto_reserva': producto_reserva,
                    'producto': producto,
                    'error': 'La cantidad introducida no es válida.'
                }
            )

        if nueva_cantidad <= 0:
            logger.warning(
                "Cantidad no válida (%s) para la reserva ID %s",
                nueva_cantidad,
                reserva_id
            )
            return render(
                request,
                'editar_reserva.html',
                {
                    'reserva': reserva,
                    'producto_reserva': producto_reserva,
                    'producto': producto,
                    'error': 'La cantidad debe ser mayor que 0.'
                }
            )

        #Las unidades reservadas vuelven a estar disponibles
        #para calcular el nuevo stock máximo.
        stock_disponible = producto.stock + cantidad_actual

        #Comprobar el stock mediante una excepción personalizada
        try:
            ValidadorStock(stock_disponible).validar(nueva_cantidad)

        except StockInsuficienteError as error:
            logger.warning(
                "Stock insuficiente al editar la reserva ID %s: %s",
                reserva_id,
                error
            )
            return render(
                request,
                'editar_reserva.html',
                {
                    'reserva': reserva,
                    'producto_reserva': producto_reserva,
                    'producto': producto,
                    'error': str(error)
                }
            )

        try:
            with transaction.atomic():
                diferencia = nueva_cantidad - cantidad_actual

                producto.stock -= diferencia
                producto.save()

                producto_reserva.cantidad = nueva_cantidad
                producto_reserva.save()

            logger.info(
                "Reserva modificada: ID %s, usuario %s, "
                "cantidad anterior %s, cantidad nueva %s",
                reserva_id,
                request.user.username,
                cantidad_actual,
                nueva_cantidad
            )

            return redirect('mis_reservas')

        except Exception:
            logger.exception(
                "Error al modificar la reserva ID %s",
                reserva_id
            )
            raise

    return render(
        request,
        'editar_reserva.html',
        {
            'reserva': reserva,
            'producto_reserva': producto_reserva,
            'producto': producto
        }
    )


#Vista para eliminar una reserva
@login_required
def eliminar_reserva(request, reserva_id):
    """Elimina una reserva y devuelve las unidades al stock."""
    reserva = get_object_or_404(
        Reserva,
        id=reserva_id,
        usuario=request.user
    )

    if request.method == 'POST':
        try:
            with transaction.atomic():
                productos_reserva = reserva.productos.all()

                for producto_reserva in productos_reserva:
                    producto = producto_reserva.producto
                    producto.stock += producto_reserva.cantidad
                    producto.save()

                usuario_reserva = reserva.usuario.username
                reserva.delete()

            logger.info(
                "Reserva eliminada: ID %s, usuario %s",
                reserva_id,
                usuario_reserva
            )

            return redirect('mis_reservas')

        except Exception:
            logger.exception(
                "Error al eliminar la reserva ID %s",
                reserva_id
            )
            raise

    return render(
        request,
        'confirmar_eliminacion_reserva.html',
        {
            'reserva': reserva
        }
    )


#Vista para consultar las reservas del usuario
def mis_reservas(request):
    """Muestra las reservas del usuario autenticado."""
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
