from django.db import models
from pacientes.models import Paciente

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('Programada', 'Programada'),
        ('Finalizada', 'Finalizada'),
        ('Cancelada', 'Cancelada'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Programada')
    nota = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cita de {self.paciente} el {self.fecha} a las {self.hora}"
    
    class Meta:
        db_table = 'citas'
        unique_together = ('fecha', 'hora')