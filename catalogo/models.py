from django.db import models
#mi tabla de reserva este conectada con con usuarios
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


# un product de tech covers tiene nombre, descripcion, precio y stock 
#Relacion catgoria producto 1:N

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos'
    )

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"Reserva {self.id} - {self.usuario.username}"

#indicamos que productos hay qn cada reserva y cuantas unidades se han reservado
class ProductoReserva(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE,
        related_name='productos'
    )
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad}"
