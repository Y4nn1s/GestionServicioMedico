from django import forms
from django.core.validators import RegexValidator
from .models import Categoria, Proveedor, Medicamento, Inventario

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

class ProveedorForm(forms.ModelForm):
    # Validador para teléfono
    telefono_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe tener entre 9 y 15 dígitos."
    )
    
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefono'].validators.append(self.telefono_validator)
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre', 'descripcion', 'categoria', 'proveedor', 'precio_unitario', 'stock_minimo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')
        if precio <= 0:
            raise forms.ValidationError("El precio unitario debe ser mayor que cero.")
        return precio
    
    def clean_stock_minimo(self):
        stock = self.cleaned_data.get('stock_minimo')
        if stock < 0:
            raise forms.ValidationError("El stock mínimo no puede ser negativo.")
        return stock

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['medicamento', 'cantidad', 'fecha_caducidad', 'lote']
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_caducidad': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lote': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")
        return cantidad
    
    def clean_fecha_caducidad(self):
        fecha_caducidad = self.cleaned_data.get('fecha_caducidad')
        from datetime import date
        if fecha_caducidad < date.today():
            raise forms.ValidationError("La fecha de caducidad no puede ser anterior a la fecha actual.")
        return fecha_caducidad