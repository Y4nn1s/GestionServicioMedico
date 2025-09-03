from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'edad', 'genero', 'telefono')
    list_filter = ('genero', 'edad')
    search_fields = ('nombre', 'apellido', 'cedula')