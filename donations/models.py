from django.db import models
import uuid

class Donacion(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
    max_length=20,
    choices=[
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado')
    ],
        default='pendiente'
    )
    
    referencia = models.CharField(max_length=100, unique=True, editable=False)
    
    comprobante = models.ImageField(upload_to='comprobantes/')

    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.referencia:
            self.referencia = str(uuid.uuid4()).split('-')[0].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.referencia}"
    