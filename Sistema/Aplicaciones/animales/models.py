from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Usuario(AbstractUser):
    ROLES = (
        ('administrador', 'Administrador'),
        ('encargado', 'Encargado'),
        ('revisor', 'Revisor'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)
    
    # Evitar conflictos con auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='usuario_groups',  # <-- cambia el related_name
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        verbose_name='grupos'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_user_permissions',  # <-- cambia el related_name
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='permisos de usuario'
    )

    def __str__(self):
        return self.username


# =============================
# Animal simplificado con foto
# =============================
class Animal(models.Model):
    tipo = models.CharField(max_length=20)  # vaca, toro, becerro
    sexo = models.CharField(max_length=1, choices=(('M','M'),('F','F')))
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to='animales/', blank=True, null=True)  # carpeta media/animales/

    def __str__(self):
        return f"{self.tipo} - {self.id}"


# =============================
# Evento
# =============================
class Evento(models.Model):
    TIPO_EVENTO = (
        ('nacimiento', 'Nacimiento'),
        ('vacunacion', 'Vacunación'),
        ('enfermedad', 'Enfermedad'),
        ('venta', 'Venta'),
        ('inseminacion', 'Inseminación'),
    )

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='eventos')
    tipo_evento = models.CharField(max_length=50, choices=TIPO_EVENTO)
    fecha_evento = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    responsable = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='eventos_responsable')

    def __str__(self):
        return f"{self.tipo_evento} - {self.animal}"


# =============================
# Producción
# =============================
class Produccion(models.Model):
    TIPO_PRODUCTO = (
        ('leche', 'Leche'),
        ('carne', 'Carne'),
    )

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='producciones')
    fecha = models.DateField()
    tipo_producto = models.CharField(max_length=20, choices=TIPO_PRODUCTO)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_producto} - {self.animal} - {self.fecha}"

class Perfil(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    nombre_completo = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    fecha_ingreso = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre_completo

