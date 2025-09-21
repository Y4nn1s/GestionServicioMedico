from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from .models import Cita, EstadoCita, TipoCita, MotivoCita
from .forms import CitaForm

def index(request):
    citas_list = Cita.objects.all().select_related('paciente', 'tipo_cita', 'motivo', 'estado').order_by('-fecha', '-hora_inicio')
    paginator = Paginator(citas_list, 10)  # Mostrar 10 citas por página
    page_number = request.GET.get('page')
    citas = paginator.get_page(page_number)
    return render(request, 'citas/index.html', {'citas': citas})

def create(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            messages.success(request, 'Cita creada correctamente.')
            return redirect('citas:index')
    else:
        form = CitaForm()
    return render(request, 'citas/create.html', {'form': form})

def show(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    notas = cita.notas.all()
    return render(request, 'citas/show.html', {
        'cita': cita,
        'notas': notas
    })

def edit(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada correctamente.')
            return redirect('citas:index')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'citas/edit.html', {'form': form, 'cita': cita})

def destroy(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    if request.method == 'POST':
        cita.delete()
        messages.success(request, 'Cita eliminada correctamente.')
        return redirect('citas:index')
    return render(request, 'citas/destroy.html', {'cita': cita})

def search(request):
    query = request.GET.get('q', '')
    citas = Cita.objects.all().select_related('paciente', 'tipo_cita', 'motivo', 'estado').order_by('-fecha', '-hora_inicio')
    
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

def citas_hoy(request):
    hoy = timezone.now().date()
    citas = Cita.objects.filter(fecha=hoy).order_by('hora_inicio')
    
    return render(request, 'citas/hoy.html', {
        'citas': citas,
        'hoy': hoy
    })

def cambiar_estado(request, cita_id, estado_id):
    cita = get_object_or_404(Cita, id=cita_id)
    estado = get_object_or_404(EstadoCita, id=estado_id)
    cita.estado = estado
    cita.save()
    messages.success(request, f'Estado de cita actualizado a {estado.nombre}.')
    return redirect('citas:show', cita_id=cita_id)