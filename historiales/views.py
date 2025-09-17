from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import HistorialMedico
from .forms import HistorialMedicoForm

def index(request):
    try:
        historiales_list = HistorialMedico.objects.all().select_related('paciente')
        paginator = Paginator(historiales_list, 10)
        page_number = request.GET.get('page')
        historiales = paginator.get_page(page_number)
        return render(request, 'historiales/index.html', {'historiales': historiales})
    except Exception as e:
        messages.error(request, f'Error al cargar los historiales: {str(e)}')
        return render(request, 'historiales/index.html', {'historiales': []})

@transaction.atomic
def create(request):
    if request.method == 'POST':
        form = HistorialMedicoForm(request.POST)
        if form.is_valid():
            try:
                historial = form.save()
                messages.success(request, 'Historial médico creado correctamente.')
                return redirect('historiales:index')
                
            except ValidationError as e:
                messages.error(request, f'Error de validación: {", ".join(e.messages)}')
            except IntegrityError as e:
                messages.error(request, 'Error de integridad de datos. El paciente ya tiene un historial médico.')
            except Exception as e:
                messages.error(request, f'Error inesperado al crear el historial: {str(e)}')
                raise
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = HistorialMedicoForm()
    
    return render(request, 'historiales/create.html', {'form': form})

def show(request, historial_id):
    try:
        historial = get_object_or_404(HistorialMedico, id=historial_id)
        return render(request, 'historiales/show.html', {'historial': historial})
    except Exception as e:
        messages.error(request, f'Error al cargar el historial: {str(e)}')
        return redirect('historiales:index')

@transaction.atomic
def edit(request, historial_id):
    historial = get_object_or_404(HistorialMedico, id=historial_id)
    
    if request.method == 'POST':
        form = HistorialMedicoForm(request.POST, instance=historial)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Historial médico actualizado correctamente.')
                return redirect('historiales:index')
                
            except ValidationError as e:
                messages.error(request, f'Error de validación: {", ".join(e.messages)}')
            except IntegrityError as e:
                messages.error(request, 'Error de integridad de datos.')
            except Exception as e:
                messages.error(request, f'Error inesperado al actualizar el historial: {str(e)}')
                raise
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = HistorialMedicoForm(instance=historial)
    
    return render(request, 'historiales/edit.html', {'form': form, 'historial': historial})

@transaction.atomic
def destroy(request, historial_id):
    historial = get_object_or_404(HistorialMedico, id=historial_id)
    
    if request.method == 'POST':
        try:
            # Guardar información para el mensaje antes de eliminar
            paciente_info = str(historial.paciente)
            historial.delete()
            
            messages.success(request, f'Historial médico de {paciente_info} eliminado correctamente.')
            return redirect('historiales:index')
            
        except Exception as e:
            messages.error(request, f'Error al eliminar el historial médico: {str(e)}')
            return redirect('historiales:show', historial_id=historial_id)
    
    return render(request, 'historiales/destroy.html', {'historial': historial})

def search(request):
    try:
        query = request.GET.get('q', '')
        historiales = HistorialMedico.objects.all().select_related('paciente')
        
        if query:
            historiales = historiales.filter(
                Q(paciente__nombre__icontains=query) |
                Q(paciente__apellido__icontains=query) |
                Q(alergias__icontains=query) |
                Q(enfermedades_preexistentes__icontains=query) |
                Q(medicamentos_actuales__icontains=query)
            )
        
        paginator = Paginator(historiales, 10)
        page_number = request.GET.get('page')
        historiales_page = paginator.get_page(page_number)
        
        return render(request, 'historiales/search.html', {
            'historiales': historiales_page,
            'query': query
        })
    except Exception as e:
        messages.error(request, f'Error en la búsqueda: {str(e)}')
        return redirect('historiales:index')