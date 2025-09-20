from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import HistorialMedico
from .forms import HistorialMedicoForm

def index(request):
    historiales_list = HistorialMedico.objects.all().order_by('-created_at')
    paginator = Paginator(historiales_list, 10)  # Mostrar 10 historiales por página
    page_number = request.GET.get('page')
    historiales = paginator.get_page(page_number)
    return render(request, 'historiales/index.html', {'historiales': historiales})

def create(request):
    if request.method == 'POST':
        form = HistorialMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Historial médico creado correctamente.')
            return redirect('historiales:index')
    else:
        form = HistorialMedicoForm()
    return render(request, 'historiales/create.html', {'form': form})

def show(request, historial_id):
    historial = get_object_or_404(HistorialMedico, id=historial_id)
    return render(request, 'historiales/show.html', {'historial': historial})

def edit(request, historial_id):
    historial = get_object_or_404(HistorialMedico, id=historial_id)
    if request.method == 'POST':
        form = HistorialMedicoForm(request.POST, instance=historial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Historial médico actualizado correctamente.')
            return redirect('historiales:index')
    else:
        form = HistorialMedicoForm(instance=historial)
    return render(request, 'historiales/edit.html', {'form': form, 'historial': historial})

def destroy(request, historial_id):
    historial = get_object_or_404(HistorialMedico, id=historial_id)
    if request.method == 'POST':
        historial.delete()
        messages.success(request, 'Historial médico eliminado correctamente.')
        return redirect('historiales:index')
    return render(request, 'historiales/destroy.html', {'historial': historial})

def search(request):
    query = request.GET.get('q', '')
    historiales = HistorialMedico.objects.all().order_by('-created_at')
    
    if query:
        historiales = historiales.filter(
            paciente__nombre__icontains=query
        )
    
    paginator = Paginator(historiales, 10)
    page_number = request.GET.get('page')
    historiales_page = paginator.get_page(page_number)
    
    return render(request, 'historiales/search.html', {
        'historiales': historiales_page,
        'query': query
    })