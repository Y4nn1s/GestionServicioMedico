from django import forms
from django.core.exceptions import ValidationError
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
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Lista de alergias separadas por coma'}),
            'enfermedades_preexistentes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Lista de enfermedades separadas por coma'}),
            'medicamentos_actuales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Lista de medicamentos separados por coma'}),
        }
        labels = {
            'paciente': 'Paciente',
            'alergias': 'Alergias',
            'enfermedades_preexistentes': 'Enfermedades Preexistentes',
            'medicamentos_actuales': 'Medicamentos Actuales',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si es una creación (no edición), filtrar pacientes que no tienen historial
        if not self.instance.pk:
            self.fields['paciente'].queryset = Paciente.objects.filter(historialmedico__isnull=True)
        else:
            # En edición, permitir el paciente actual
            self.fields['paciente'].queryset = Paciente.objects.filter(
                historialmedico__isnull=True
            ) | Paciente.objects.filter(pk=self.instance.paciente.pk)

    def clean_paciente(self):
        paciente = self.cleaned_data.get('paciente')
        
        # Si estamos creando, validar que el paciente no tenga historial
        if not self.instance.pk and paciente and hasattr(paciente, 'historialmedico'):
            raise ValidationError('Este paciente ya tiene un historial médico.')
            
        return paciente

    def clean(self):
        cleaned_data = super().clean()
        alergias = cleaned_data.get('alergias', '')
        enfermedades_preexistentes = cleaned_data.get('enfermedades_preexistentes', '')
        medicamentos_actuales = cleaned_data.get('medicamentos_actuales', '')
        
        # Validar que al menos un campo tenga información
        if not alergias and not enfermedades_preexistentes and not medicamentos_actuales:
            raise ValidationError('Debe completar al menos uno de los campos: Alergias, Enfermedades Preexistentes o Medicamentos Actuales.')
            
        return cleaned_data