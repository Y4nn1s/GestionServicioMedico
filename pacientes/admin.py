from django.contrib import admin
from .models import Paciente, TipoDocumento, Genero, Pais, Departamento, Ciudad, TipoTelefono, Direccion, Telefono

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_iso')
    search_fields = ('nombre', 'codigo_iso')

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais')
    list_filter = ('pais',)
    search_fields = ('nombre',)

@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento')
    list_filter = ('departamento__pais', 'departamento')
    search_fields = ('nombre',)

@admin.register(TipoTelefono)
class TipoTelefonoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'mascara')
    search_fields = ('nombre',)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'numero_documento', 'fecha_nacimiento', 'genero', 'email')
    list_filter = ('genero', 'tipo_documento')
    search_fields = ('nombre', 'apellido', 'numero_documento')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'ciudad', 'direccion', 'es_principal')
    list_filter = ('ciudad__departamento__pais', 'ciudad__departamento', 'ciudad', 'es_principal')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'direccion')

@admin.register(Telefono)
class TelefonoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'tipo_telefono', 'numero', 'es_principal')
    list_filter = ('tipo_telefono', 'es_principal')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'numero')