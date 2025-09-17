from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Paciente, TipoDocumento, Genero

class PacienteForm(forms.ModelForm):
    confirmar_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Repita el correo electrónico'}),
        label="Confirmar Email"
    )
    
    class Meta:
        model = Paciente
        fields = [
            'tipo_documento',
            'numero_documento',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'genero',
            'email',
        ]
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solo números y letras'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pérez'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'max': timezone.now().date()}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
        }
        labels = {
            'tipo_documento': 'Tipo de Documento',
            'numero_documento': 'Número de Documento',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'genero': 'Género',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_documento'].queryset = TipoDocumento.objects.all()
        self.fields['genero'].queryset = Genero.objects.all()
        
        # Establecer fecha máxima para fecha de nacimiento (hoy)
        self.fields['fecha_nacimiento'].widget.attrs['max'] = timezone.now().date()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirmar_email = cleaned_data.get('confirmar_email')
        
        # Validar que los emails coincidan si ambos están proporcionados
        if email and confirmar_email and email != confirmar_email:
            raise ValidationError('Los correos electrónicos no coinciden.')
            
        return cleaned_data

    def clean_numero_documento(self):
        tipo_documento = self.cleaned_data.get('tipo_documento')
        numero_documento = self.cleaned_data.get('numero_documento')
        
        if tipo_documento and numero_documento:
            # Verificar si ya existe un paciente con el mismo tipo y número de documento
            pacientes_existentes = Paciente.objects.filter(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento
            )
            
            # Excluir la instancia actual si estamos editando
            if self.instance and self.instance.pk:
                pacientes_existentes = pacientes_existentes.exclude(pk=self.instance.pk)
                
            if pacientes_existentes.exists():
                raise ValidationError('Ya existe un paciente con este tipo y número de documento.')
                
        return numero_documento

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        
        if fecha_nacimiento:
            # Validar que la fecha de nacimiento no sea futura
            if fecha_nacimiento > timezone.now().date():
                raise ValidationError('La fecha de nacimiento no puede ser futura.')
                
            # Validar que el paciente tenga al menos 1 año (opcional)
            edad = (timezone.now().date() - fecha_nacimiento).days / 365
            if edad < 1:
                raise ValidationError('El paciente debe tener al menos 1 año de edad.')
                
        return fecha_nacimiento

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email:
            # Verificar si el email ya está en uso por otro paciente
            pacientes_existentes = Paciente.objects.filter(email=email)
            
            # Excluir la instancia actual si estamos editando
            if self.instance and self.instance.pk:
                pacientes_existentes = pacientes_existentes.exclude(pk=self.instance.pk)
                
            if pacientes_existentes.exists():
                raise ValidationError('Este correo electrónico ya está registrado.')
                
        return email