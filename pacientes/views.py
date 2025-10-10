from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction
from .models import Paciente, TipoDocumento, Estado, Ciudad, Direccion, Telefono, TipoTelefono, Pais
from .forms import PacienteForm, DireccionFormSet, TelefonoFormSet
from .forms import DireccionForm, TelefonoForm

def index(request):
    pacientes_list = Paciente.objects.all().order_by('apellido', 'nombre')
    paginator = Paginator(pacientes_list, 10)  # Mostrar 10 pacientes por página
    page_number = request.GET.get('page')
    pacientes = paginator.get_page(page_number)
    return render(request, 'pacientes/index.html', {'pacientes': pacientes})


@transaction.atomic
def create(request):
    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST)
        direccion_formset = DireccionFormSet(request.POST)
        telefono_formset = TelefonoFormSet(request.POST)
        
        # Imprimir errores para debugging
        if not paciente_form.is_valid():
            print("Errores en paciente_form:", paciente_form.errors)
        if not direccion_formset.is_valid():
            print("Errores en direccion_formset:", direccion_formset.errors)
        if not telefono_formset.is_valid():
            print("Errores en telefono_formset:", telefono_formset.errors)
        
        # Cargar los querysets para los formularios de dirección
        for form in direccion_formset:
            if form.is_bound:
                # Si el formulario está bound, cargar los querysets según los datos enviados
                ciudad_id = request.POST.get(form.prefix + '-ciudad')
                if ciudad_id:
                    try:
                        ciudad = Ciudad.objects.get(id=ciudad_id)
                        estado = ciudad.estado
                        pais = estado.pais
                        form.fields['ciudad'].queryset = Ciudad.objects.filter(estado=estado)
                    except Ciudad.DoesNotExist:
                        pass  # El formulario mostrará el error de validación
        
        if paciente_form.is_valid() and direccion_formset.is_valid() and telefono_formset.is_valid():
            try:
                paciente = paciente_form.save()
                direccion_formset.instance = paciente
                direccion_formset.save()
                telefono_formset.instance = paciente
                telefono_formset.save()
                messages.success(request, 'Paciente creado correctamente.')
                return redirect('pacientes:index')
            except Exception as e:
                messages.error(request, f'Error al crear el paciente: {str(e)}')
                print("Error al crear el paciente:", str(e))
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        paciente_form = PacienteForm()
        direccion_formset = DireccionFormSet()
        telefono_formset = TelefonoFormSet()
    
    # Obtener datos para los selects dinámicos
    paises = Pais.objects.all().order_by('nombre')
    
    return render(request, 'pacientes/create.html', {
        'form': paciente_form,
        'direccion_formset': direccion_formset,
        'telefono_formset': telefono_formset,
        'paises': paises,
    })

def show(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    direcciones = Direccion.objects.filter(paciente=paciente).select_related('ciudad__estado__pais')
    telefonos = Telefono.objects.filter(paciente=paciente).select_related('tipo_telefono')
    return render(request, 'pacientes/show.html', {
        'paciente': paciente,
        'direcciones': direcciones,
        'telefonos': telefonos
    })


@transaction.atomic
def edit(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST, instance=paciente)
        direccion_formset = DireccionFormSet(request.POST, instance=paciente)
        telefono_formset = TelefonoFormSet(request.POST, instance=paciente)
        
        if paciente_form.is_valid() and direccion_formset.is_valid() and telefono_formset.is_valid():
            paciente_form.save()
            direccion_formset.save()
            telefono_formset.save()
            messages.success(request, 'Paciente actualizado correctamente.')
            return redirect('pacientes:index')
    else:
        paciente_form = PacienteForm(instance=paciente)
        direccion_formset = DireccionFormSet(instance=paciente)
        telefono_formset = TelefonoFormSet(instance=paciente)
    
    # Obtener datos para los selects dinámicos
    paises = Pais.objects.all().order_by('nombre')
    
    # Cargar datos iniciales para los formularios de dirección
    for form in direccion_formset:
        if form.instance and form.instance.pk:
            # Si el formulario tiene una instancia existente, cargar los datos relacionados
            if hasattr(form.instance, 'ciudad') and form.instance.ciudad:
                ciudad = form.instance.ciudad
                estado = ciudad.estado
                pais = estado.pais
                # Cargar ciudades disponibles para el estado
                form.fields['ciudad'].queryset = Ciudad.objects.filter(estado=estado)
                # Establecer la ciudad existente como inicial
                form.fields['ciudad'].initial = ciudad
            else:
                # Si no hay ciudad asociada, cargar todas las ciudades
                form.fields['ciudad'].queryset = Ciudad.objects.all()
        else:
            # Para formularios nuevos, cargar todas las ciudades
            form.fields['ciudad'].queryset = Ciudad.objects.all()
    
    # Cargar datos iniciales para los formularios de teléfono
    for form in telefono_formset:
        if form.instance and form.instance.pk:
            # Los datos ya deberían cargarse automáticamente por el formset
            pass
    
    return render(request, 'pacientes/edit.html', {
        'form': paciente_form,
        'direccion_formset': direccion_formset,
        'telefono_formset': telefono_formset,
        'paciente': paciente,
        'paises': paises,
    })


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
    query = request.GET.get('q', '')
    pacientes = Paciente.objects.all().order_by('apellido', 'nombre')
    
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

# Vistas AJAX para cargar datos dinámicamente
def cargar_estados(request):
    pais_id = request.GET.get('pais_id')
    estados = Estado.objects.filter(pais_id=pais_id).order_by('nombre')
    return render(request, 'pacientes/dropdown_list_options.html', {'opciones': estados})

def cargar_ciudades(request):
    estado_id = request.GET.get('estado_id')
    ciudades = Ciudad.objects.filter(estado_id=estado_id).order_by('nombre')
    return render(request, 'pacientes/dropdown_list_options.html', {'opciones': ciudades})
