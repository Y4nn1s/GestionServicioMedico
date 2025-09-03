from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Paciente
from .forms import PacienteForm

def index(request):
    pacientes_list = Paciente.objects.all()
    paginator = Paginator(pacientes_list, 10)  # Mostrar 10 pacientes por página
    page_number = request.GET.get('page')
    pacientes = paginator.get_page(page_number)
    return render(request, 'pacientes/index.html', {'pacientes': pacientes})

def create(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente creado correctamente.')
            return redirect('pacientes:index')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/create.html', {'form': form})

def show(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    return render(request, 'pacientes/show.html', {'paciente': paciente})

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
    paciente.delete()
    messages.success(request, 'Paciente eliminado correctamente.')
    return redirect('pacientes:index')