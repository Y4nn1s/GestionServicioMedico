from django import forms
from .models import HistorialMedico
from pacientes.models import Paciente

class HistorialMedicoForm(forms.ModelForm):
    class Meta:
        model = HistorialMedico
        fields = [
            'paciente',
            'alergias',
            'enfermedades_preexistentes',
            'medicamentos_actuales',
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'enfermedades_preexistentes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medicamentos_actuales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'paciente': 'Paciente',
            'alergias': 'Alergias',
            'enfermedades_preexistentes': 'Enfermedades Preexistentes',
            'medicamentos_actuales': 'Medicamentos Actuales',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.all()
        # Si es una creación (no edición), filtrar pacientes que no tienen historial
        if not self.instance.pk:
            self.fields['paciente'].queryset = Paciente.objects.filter(historialmedico__isnull=True)