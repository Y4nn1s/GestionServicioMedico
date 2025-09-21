from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Paciente, TipoDocumento, Genero, Pais, Departamento, Ciudad, Direccion, Telefono, TipoTelefono
from .forms import PacienteForm

def index(request):
    pacientes_list = Paciente.objects.all().order_by('apellido', 'nombre')
    paginator = Paginator(pacientes_list, 10)  # Mostrar 10 pacientes por página
    page_number = request.GET.get('page')
    pacientes = paginator.get_page(page_number)
    return render(request, 'pacientes/index.html', {'pacientes': pacientes})

def create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, 'Paciente creado correctamente.')
            return redirect('pacientes:index')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/create.html', {'form': form})

def show(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    direcciones = Direccion.objects.filter(paciente=paciente)
    telefonos = Telefono.objects.filter(paciente=paciente)
    return render(request, 'pacientes/show.html', {
        'paciente': paciente,
        'direcciones': direcciones,
        'telefonos': telefonos
    })

def edit(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente actualizado correctamente.')
            return redirect('pacientes:index')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'pacientes/edit.html', {'form': form, 'paciente': paciente})

def destroy(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, 'Paciente eliminado correctamente.')
        return redirect('pacientes:index')
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