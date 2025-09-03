from django.db import models

class Paciente(models.Model):
    GENERO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    cedula = models.CharField(max_length=20)
    edad = models.IntegerField()
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        db_table = 'pacientes'