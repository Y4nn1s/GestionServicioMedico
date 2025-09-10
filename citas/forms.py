from django import forms
from .models import Cita
from pacientes.models import Paciente

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'paciente': 'Paciente',
            'fecha': 'Fecha y Hora',
            'motivo': 'Motivo de la Consulta',
            'estado': 'Estado',
            'notas': 'Notas Adicionales',
        }

class CitaFilterForm(forms.Form):
    ESTADO_CHOICES = [
        ('', 'Todos los estados'),
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    fecha = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )