from django import forms
from .models import Cita, EstadoCita, TipoCita, MotivoCita
from pacientes.models import Paciente

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            'paciente',
            'tipo_cita',
            'motivo',
            'fecha',
            'hora_inicio',
            'hora_fin',
            'estado',
            'observaciones',
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'tipo_cita': forms.Select(attrs={'class': 'form-control'}),
            'motivo': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'paciente': 'Paciente',
            'tipo_cita': 'Tipo de Cita',
            'motivo': 'Motivo',
            'fecha': 'Fecha',
            'hora_inicio': 'Hora de Inicio',
            'hora_fin': 'Hora de Fin',
            'estado': 'Estado',
            'observaciones': 'Observaciones',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.all()
        self.fields['tipo_cita'].queryset = TipoCita.objects.all()
        self.fields['motivo'].queryset = MotivoCita.objects.all()
        self.fields['estado'].queryset = EstadoCita.objects.all()