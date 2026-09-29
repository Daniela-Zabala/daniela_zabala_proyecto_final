from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Producto


# Formulario para que el usuario pueda registrarse
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        label="Correo electrónico"
    )

    class Meta:
        model = User
        fields = ['username', 'email']


# Formulario para crear o editar un producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'stock',
            'categoria'
        ]


