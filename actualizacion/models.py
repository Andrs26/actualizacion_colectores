import json
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Cliente(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Actualizado', 'Actualizado'),
        ('No Ubicado', 'No Ubicado'),
    ]

    id_zoho = models.CharField(max_length=100, unique=True)
    nombre_empresa = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    usuario_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.nombre_empresa

class ClienteDatos(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='datos')
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    pagina_web = models.URLField(blank=True)
    numero_sucursales = models.PositiveIntegerField(null=True, blank=True)
    numero_empleados = models.TextField(null=True, blank=True)
    principales_productos = models.TextField(blank=True)

class ClienteContacto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contactos')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    cargo = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
