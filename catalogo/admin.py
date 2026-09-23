#from django.contrib import admin

from django.contrib import admin
from .models import Categoria, Producto, Reserva, ProductoReserva


admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Reserva)
admin.site.register(ProductoReserva)


