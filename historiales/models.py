from django.db import models
from pacientes.models import Paciente

class HistorialMedico(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    alergias = models.TextField(blank=True, null=True)
    enfermedades_preexistentes = models.TextField(blank=True, null=True)
    medicamentos_actuales = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Historial de {self.paciente}"
    
    class Meta:
        db_table = 'historiales_medicos'