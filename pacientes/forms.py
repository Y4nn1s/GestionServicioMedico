from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Paciente, TipoDocumento, Genero, Direccion, Telefono, Ciudad, Estado, Pais, TipoTelefono


class PacienteForm(forms.ModelForm):
    confirmar_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Repita el correo electrónico'}),
        label="Confirmar Email"
    )
    
    class Meta:
        model = Paciente
        fields = [
            'numero_documento',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'genero',
            'email',
        ]
        widgets = {
            'numero_documento': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '8',
                'placeholder': 'Ej: 12345678'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '30',
                'placeholder': 'Ej: Juan Carlos'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '20',
                'placeholder': 'Ej: García López'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
        }
        labels = {
            'numero_documento': 'Número de Cédula',
            'nombre': 'Nombres',
            'apellido': 'Apellidos',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'genero': 'Género',
            'email': 'Correo Electrónico',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Establecer valores predeterminados
        if not self.instance.pk:
            self.fields['genero'].initial = Genero.MASCULINO
        
        # Formatear correctamente la fecha de nacimiento si existe
        if self.instance and self.instance.fecha_nacimiento:
            self.fields['fecha_nacimiento'].widget.attrs['value'] = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')

    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get('numero_documento')
        if numero_documento:
            if not numero_documento.isdigit():
                raise ValidationError('El número de cédula solo debe contener dígitos.')
            if len(numero_documento) != 8:
                raise ValidationError('El número de cédula debe tener exactamente 8 dígitos.')
        return numero_documento

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            if not nombre.replace(' ', '').isalpha():
                raise ValidationError('Los nombres solo deben contener letras y espacios.')
            if len(nombre) > 30:
                raise ValidationError('El nombre no debe exceder los 30 caracteres.')
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if apellido:
            if not apellido.replace(' ', '').isalpha():
                raise ValidationError('Los apellidos solo deben contener letras y espacios.')
            if len(apellido) > 20:
                raise ValidationError('El apellido no debe exceder los 20 caracteres.')
        return apellido

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['ciudad', 'direccion', 'codigo_postal']
        widgets = {
            'ciudad': forms.Select(attrs={'class': 'form-control mb-2 ciudad-select'}),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Ej: Av. Principal, Calle 1, Casa 123'
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Ej: 1010',
                'maxlength': '4'
            }),
        }
        labels = {
            'direccion': 'Dirección',
            'codigo_postal': 'Código Postal',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar el queryset de ciudades con todas las ciudades disponibles
        self.fields['ciudad'].queryset = Ciudad.objects.select_related('estado__pais').all()

    def clean_ciudad(self):
        ciudad = self.cleaned_data.get('ciudad')
        direccion = self.cleaned_data.get('direccion')
        
        # Solo validar si se ha ingresado una dirección
        if direccion and not ciudad:
            raise ValidationError("Debe seleccionar una ciudad cuando ingresa una dirección.")
            
        return ciudad

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        ciudad = self.cleaned_data.get('ciudad')
        
        # Solo validar si se ha seleccionado una ciudad
        if ciudad and not direccion:
            raise ValidationError("Debe ingresar una dirección cuando selecciona una ciudad.")
            
        return direccion

    def clean(self):
        cleaned_data = super().clean()
        ciudad = cleaned_data.get('ciudad')
        direccion = cleaned_data.get('direccion')
        
        # Validación adicional para asegurar consistencia
        if direccion and not ciudad:
            raise ValidationError("Debe seleccionar una ciudad cuando ingresa una dirección.")
        elif ciudad and not direccion:
            raise ValidationError("Debe ingresar una dirección cuando selecciona una ciudad.")
            
        return cleaned_data

class TelefonoForm(forms.ModelForm):
    class Meta:
        model = Telefono
        fields = ['tipo_telefono', 'numero', 'es_principal']
        widgets = {
            'tipo_telefono': forms.Select(attrs={'class': 'form-control mb-2'}),
            'numero': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Ej: 04121234567',
                'maxlength': '11'
            }),
            'es_principal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'tipo_telefono': 'Tipo de Teléfono',
            'numero': 'Número',
            'es_principal': 'Teléfono Principal',
        }

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if numero:
            if len(numero) != 11:
                raise ValidationError('El número de teléfono debe tener exactamente 11 dígitos.')
            if not numero.isdigit():
                raise ValidationError('El número de teléfono solo debe contener dígitos.')
        return numero

# Formsets para manejar múltiples direcciones y teléfonos
DireccionFormSet = inlineformset_factory(
    Paciente, Direccion, form=DireccionForm,
    extra=1, can_delete=True,
    fields=['ciudad', 'direccion', 'codigo_postal']
)

TelefonoFormSet = inlineformset_factory(
    Paciente, Telefono, form=TelefonoForm,
    extra=1, can_delete=True,
    fields=['tipo_telefono', 'numero', 'es_principal']
)
