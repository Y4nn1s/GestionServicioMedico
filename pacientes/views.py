from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import Paciente, TipoDocumento, Genero, Direccion, Telefono
from .forms import PacienteForm
from historiales.models import HistorialMedico

def index(request):
    try:
        pacientes_list = Paciente.objects.all().select_related('tipo_documento', 'genero')
        paginator = Paginator(pacientes_list, 10)
        page_number = request.GET.get('page')
        pacientes = paginator.get_page(page_number)
        return render(request, 'pacientes/index.html', {'pacientes': pacientes})
    except Exception as e:
        messages.error(request, f'Error al cargar los pacientes: {str(e)}')
        return render(request, 'pacientes/index.html', {'pacientes': []})

@transaction.atomic
def create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            try:
                paciente = form.save()
                
                # Crear historial médico vacío automáticamente
                HistorialMedico.objects.create(paciente=paciente)
                
                messages.success(request, 'Paciente creado correctamente con historial médico.')
                return redirect('pacientes:index')
                
            except ValidationError as e:
                messages.error(request, f'Error de validación: {", ".join(e.messages)}')
            except IntegrityError as e:
                messages.error(request, 'Error de integridad de datos. Ya existe un paciente con este documento.')
            except Exception as e:
                messages.error(request, f'Error inesperado al crear el paciente: {str(e)}')
                raise
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = PacienteForm()
    
    return render(request, 'pacientes/create.html', {'form': form})

def show(request, paciente_id):
    try:
        paciente = get_object_or_404(Paciente, id=paciente_id)
        direcciones = Direccion.objects.filter(paciente=paciente).select_related('ciudad')
        telefonos = Telefono.objects.filter(paciente=paciente).select_related('tipo_telefono')
        
        return render(request, 'pacientes/show.html', {
            'paciente': paciente,
            'direcciones': direcciones,
            'telefonos': telefonos
        })
    except Exception as e:
        messages.error(request, f'Error al cargar el paciente: {str(e)}')
        return redirect('pacientes:index')

@transaction.atomic
def edit(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Paciente actualizado correctamente.')
                return redirect('pacientes:index')
                
            except ValidationError as e:
                messages.error(request, f'Error de validación: {", ".join(e.messages)}')
            except IntegrityError as e:
                messages.error(request, 'Error de integridad de datos. El documento ya está en uso por otro paciente.')
            except Exception as e:
                messages.error(request, f'Error inesperado al actualizar el paciente: {str(e)}')
                raise
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = PacienteForm(instance=paciente)
    
    return render(request, 'pacientes/edit.html', {'form': form, 'paciente': paciente})

@transaction.atomic
def destroy(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        try:
            # Guardar información para el mensaje antes de eliminar
            paciente_info = f"{paciente.nombre} {paciente.apellido}"
            paciente.delete()
            
            messages.success(request, f'Paciente {paciente_info} eliminado correctamente.')
            return redirect('pacientes:index')
            
        except Exception as e:
            messages.error(request, f'Error al eliminar el paciente: {str(e)}')
            return redirect('pacientes:show', paciente_id=paciente_id)
    
    return render(request, 'pacientes/destroy.html', {'paciente': paciente})

def search(request):
    try:
        query = request.GET.get('q', '')
        pacientes = Paciente.objects.all().select_related('tipo_documento', 'genero')
        
        if query:
            pacientes = pacientes.filter(
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query) |
                Q(numero_documento__icontains=query)
            )
        
        paginator = Paginator(pacientes, 10)
        page_number = request.GET.get('page')
        pacientes_page = paginator.get_page(page_number)
        
        return render(request, 'pacientes/search.html', {
            'pacientes': pacientes_page,
            'query': query
        })
    except Exception as e:
        messages.error(request, f'Error en la búsqueda: {str(e)}')
        return redirect('pacientes:index')