"""Formularios para el registro de usuarios y la gestión de productos."""


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Producto


# Formulario para que el usuario pueda registrarse
class RegistroUsuarioForm(UserCreationForm):
    """Formulario para registrar nuevos usuarios."""

    email = forms.EmailField(
        required=False,
        label="Correo electrónico"
    )

    class Meta:
        model = User
        fields = ['username', 'email']


# Formulario para crear o editar un producto
class ProductoForm(forms.ModelForm):
    """Formulario para crear y editar productos."""
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'stock',
            'categoria'
        ]


