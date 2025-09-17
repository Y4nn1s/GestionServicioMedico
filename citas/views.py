from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseServerError

from .models import Cita, EstadoCita, TipoCita, MotivoCita, NotaCita, TipoNota
from .forms import CitaForm

def index(request):
    citas_list = Cita.objects.all().select_related('paciente', 'tipo_cita', 'motivo', 'estado')
    paginator = Paginator(citas_list, 10)
    page_number = request.GET.get('page')
    citas = paginator.get_page(page_number)
    return render(request, 'citas/index.html', {'citas': citas})

@transaction.atomic
def create(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            try:
                cita = form.save()
                
                # Crear nota automática de creación
                tipo_nota, created = TipoNota.objects.get_or_create(
                    nombre='Sistema',
                    defaults={'descripcion': 'Notas generadas automáticamente por el sistema'}
                )
                
                NotaCita.objects.create(
                    cita=cita,
                    tipo_nota=tipo_nota,
                    contenido=f"Cita creada el {timezone.now().strftime('%Y-%m-%d %H:%M')}"
                )
                
                messages.success(request, 'Cita creada correctamente.')
                return redirect('citas:index')
                
            except ValidationError as e:
                messages.error(request, f'Error de validación: {", ".join(e.messages)}')
            except IntegrityError as e:
                messages.error(request, 'Error de integridad de datos. La cita podría solaparse con otra existente.')
            except Exception as e:
                messages.error(request, f'Error inesperado al crear la cita: {str(e)}')
                # Re-lanzar la excepción para que se revierta la transacción
                raise
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = CitaForm()
    
    return render(request, 'citas/create.html', {'form': form})

def show(request, cita_id):
    try:
        cita = get_object_or_404(Cita, id=cita_id)
        notas = cita.notas.all().select_related('tipo_nota')
        return render(request, 'citas/show.html', {
            'cita': cita,
            'notas': notas
        })
    except Exception as e:
        messages.error(request, f'Error al cargar la cita: {str(e)}')
        return redirect('citas:index')

@transaction.atomic
def edit(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            try:
                form.save()
                
                # Crear nota de edición
                tipo_nota, created = TipoNota.objects.get_or_create(
                    nombre='Sistema',
                    defaults={'descripcion': 'Notas generadas automáticamente por el sistema'}
                )
                
                NotaCita.objects.create(
                    cita=cita,
                    tipo_nota=tipo_nota,
                    contenido=f"Cita modificada el {timezone.now().strftime('%Y-%m-%d %H:%M')}"
                )
                
                messages.success(request, 'Cita actualizada correctamente.')
                return redirect('citas:index')
                
            except ValidationError as e:
                messages.error(request, f'Error de validación: {", ".join(e.messages)}')
            except IntegrityError as e:
                messages.error(request, 'Error de integridad de datos. La cita podría solaparse con otra existente.')
            except Exception as e:
                messages.error(request, f'Error inesperado al actualizar la cita: {str(e)}')
                raise
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = CitaForm(instance=cita)
    
    return render(request, 'citas/edit.html', {'form': form, 'cita': cita})

@transaction.atomic
def destroy(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    
    if request.method == 'POST':
        try:
            # Guardar información para el mensaje antes de eliminar
            cita_info = f"Cita de {cita.paciente} el {cita.fecha}"
            cita.delete()
            
            messages.success(request, f'{cita_info} eliminada correctamente.')
            return redirect('citas:index')
            
        except Exception as e:
            messages.error(request, f'Error al eliminar la cita: {str(e)}')
            return redirect('citas:show', cita_id=cita_id)
    
    return render(request, 'citas/destroy.html', {'cita': cita})

def search(request):
    try:
        query = request.GET.get('q', '')
        citas = Cita.objects.all().select_related('paciente', 'tipo_cita', 'motivo', 'estado')
        
        if query:
            citas = citas.filter(
                Q(paciente__nombre__icontains=query) |
                Q(paciente__apellido__icontains=query) |
                Q(motivo__nombre__icontains=query)
            )
        
        paginator = Paginator(citas, 10)
        page_number = request.GET.get('page')
        citas_page = paginator.get_page(page_number)
        
        return render(request, 'citas/search.html', {
            'citas': citas_page,
            'query': query
        })
    except Exception as e:
        messages.error(request, f'Error en la búsqueda: {str(e)}')
        return redirect('citas:index')

def citas_hoy(request):
    try:
        hoy = timezone.now().date()
        citas = Cita.objects.filter(fecha=hoy).select_related(
            'paciente', 'estado', 'motivo'
        ).order_by('hora_inicio')
        
        return render(request, 'citas/hoy.html', {
            'citas': citas,
            'hoy': hoy
        })
    except Exception as e:
        messages.error(request, f'Error al cargar las citas de hoy: {str(e)}')
        return redirect('citas:index')

@transaction.atomic
def cambiar_estado(request, cita_id, estado_id):
    try:
        cita = get_object_or_404(Cita, id=cita_id)
        estado = get_object_or_404(EstadoCita, id=estado_id)
        
        # Guardar el estado anterior para la nota
        estado_anterior = cita.estado.nombre
        
        cita.estado = estado
        cita.save()
        
        # Crear nota de cambio de estado
        tipo_nota, created = TipoNota.objects.get_or_create(
            nombre='Sistema',
            defaults={'descripcion': 'Notas generadas automáticamente por el sistema'}
        )
        
        NotaCita.objects.create(
            cita=cita,
            tipo_nota=tipo_nota,
            contenido=f"Estado cambiado de '{estado_anterior}' a '{estado.nombre}' el {timezone.now().strftime('%Y-%m-%d %H:%M')}"
        )
        
        messages.success(request, f'Estado de cita actualizado a {estado.nombre}.')
        
    except ValidationError as e:
        messages.error(request, f'Error de validación: {", ".join(e.messages)}')
    except IntegrityError as e:
        messages.error(request, 'Error de integridad de datos al cambiar el estado.')
    except Exception as e:
        messages.error(request, f'Error inesperado al cambiar el estado: {str(e)}')
    
    return redirect('citas:show', cita_id=cita_id)