from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_registro': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'cedula': 'Cédula',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'genero': 'Género',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
            'direccion': 'Dirección',
            'fecha_registro': 'Fecha de Registro',
        }

class PacienteSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Buscar paciente',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre, apellido o cédula...'
        })
    )