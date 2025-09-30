from django import forms
from django.forms import inlineformset_factory
from .models import Paciente, TipoDocumento, Genero, Direccion, Telefono, Ciudad, Estado, Pais, TipoTelefono

class PacienteForm(forms.ModelForm):
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
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'numero_documento': 'Número de Documento',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'genero': 'Género',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer valores predeterminados
        if not self.instance.pk:
            self.fields['genero'].initial = Genero.MASCULINO

class DireccionForm(forms.ModelForm):
    # Campo personalizado para selección jerárquica de ubicación
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-2 pais-select'})
    )
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-2 estado-select'})
    )
    
    class Meta:
        model = Direccion
        fields = ['ciudad', 'direccion', 'codigo_postal']
        widgets = {
            'ciudad': forms.Select(attrs={'class': 'form-control mb-2 ciudad-select'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control mb-2'}),
        }
        labels = {
            'direccion': 'Dirección',
            'codigo_postal': 'Código Postal',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar campos jerárquicos
        if 'initial' in kwargs:
            ciudad = kwargs['initial'].get('ciudad')
            if ciudad:
                estado = ciudad.estado
                self.fields['estado'].queryset = Estado.objects.filter(pais=estado.pais)
                self.fields['ciudad'].queryset = Ciudad.objects.filter(estado=estado)
        elif self.instance and self.instance.pk and self.instance.ciudad:
            estado = self.instance.ciudad.estado
            pais = estado.pais
            self.fields['estado'].queryset = Estado.objects.filter(pais=pais)
            self.fields['ciudad'].queryset = Ciudad.objects.filter(estado=estado)
            self.fields['pais'].initial = pais

    def clean(self):
        cleaned_data = super().clean()
        ciudad = cleaned_data.get('ciudad')
        direccion = cleaned_data.get('direccion')
        
        # Validar que si hay dirección, debe haber ciudad
        if direccion and not ciudad:
            raise forms.ValidationError("Debe seleccionar una ciudad cuando ingresa una dirección.")
            
        # Validar que si hay ciudad, debe haber dirección
        if ciudad and not direccion:
            raise forms.ValidationError("Debe ingresar una dirección cuando selecciona una ciudad.")
            
        return cleaned_data

class TelefonoForm(forms.ModelForm):
    class Meta:
        model = Telefono
        fields = ['tipo_telefono', 'numero', 'es_principal']
        widgets = {
            'tipo_telefono': forms.Select(attrs={'class': 'form-control mb-2'}),
            'numero': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'es_principal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'tipo_telefono': 'Tipo de Teléfono',
            'numero': 'Número',
            'es_principal': 'Teléfono Principal',
        }

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