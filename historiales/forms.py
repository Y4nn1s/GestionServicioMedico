from django import forms
from .models import HistorialMedico

class HistorialMedicoForm(forms.ModelForm):
    class Meta:
        model = HistorialMedico
        fields = '__all__'
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'fecha_consulta': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo_consulta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sintomas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medicamentos_recetados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'paciente': 'Paciente',
            'fecha_consulta': 'Fecha de Consulta',
            'motivo_consulta': 'Motivo de Consulta',
            'sintomas': 'Síntomas',
            'diagnostico': 'Diagnóstico',
            'tratamiento': 'Tratamiento',
            'medicamentos_recetados': 'Medicamentos Recetados',
            'notas': 'Notas Adicionales',
        }

class HistorialSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Buscar en historiales',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por paciente, diagnóstico o tratamiento...'
        })
    )