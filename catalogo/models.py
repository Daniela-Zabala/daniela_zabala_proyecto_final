#from django.db import models

# Create your models here.
from django.db import models

# Cada Clase Python en este archivo será una Tabla en la Base de Datos
class producto(models.Model):
    # Django asigna un 'id' numérico automático, ¡no lo escribas!
    
    # Definimos los campos como variables de clase con Tipado Estricto del ORM:
    titulo = models.CharField(max_length=200)
    autor_str = models.CharField(max_length=100) # (Veremos relaciones formales más abajo)
    anio = models.IntegerField(verbose_name="Año de publicación")

    # Esta función 'dunder' (doble guión bajo) es vital en Django.
    # Decide cómo se llamará el objeto en el panel visual del administrador.
    def __str__(self):
        return f"{self.titulo} ({self.autor_str})"
