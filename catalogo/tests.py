from django.test import TestCase
from .models import Categoria, Producto, Reserva, Producto_reserva
from django.contrib.auth.models import User


# Create your tests here.
class ModelosTechCoversTest(TestCase):
    """Pruebas  de los modelos de TechCovers."""

    def setUp(self):
        """Crea los datos necesarios para las pruebas."""
        self.usuario = User.objects.create_user(
            username='usuario_prueba',
            password='PruebaSegura123!'
        )

        self.categoria = Categoria.objects.create(
            nombre='Protección',
            descripcion='Accesorios de protección para móviles'
        )

        self.producto = Producto.objects.create(
            nombre='Funda de prueba',
            descripcion='Funda para un dispositivo móvil',
            precio='19.99',
            stock=10,
            categoria=self.categoria
        )

        self.reserva = Reserva.objects.create(
            usuario=self.usuario,
            estado='Pendiente'
        )

        self.producto_reserva = Producto_reserva.objects.create(
            producto=self.producto,
            reserva=self.reserva,
            cantidad=2
        )


    def test_nombre_categoria(self):
            """Comprueba la representación de una categoría."""
            self.assertEqual(str(self.categoria), 'Protección')

    def test_nombre_producto(self):
            """Comprueba la representación de un producto."""
            self.assertEqual(str(self.producto), 'Funda de prueba')

    def test_reserva_asociada_usuario(self):
            """Comprueba que la reserva pertenece al usuario correcto."""
            self.assertEqual(self.reserva.usuario, self.usuario)

    def test_producto_asociado_reserva(self):
            """Comprueba la cantidad del producto reservado."""
            self.assertEqual(self.producto_reserva.cantidad, 2)
            self.assertEqual(
                self.producto_reserva.producto,
                self.producto
            )

    def test_relacion_categoria_producto(self):
            """Comprueba la relación entre categoría y producto."""
            self.assertEqual(
                self.producto.categoria,
                self.categoria
            )
            self.assertIn(
                self.producto,
                self.categoria.productos.all()
            )
