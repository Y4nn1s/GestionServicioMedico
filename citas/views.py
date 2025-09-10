from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Cita
from .forms import CitaForm

class CitaListView(ListView):
    model = Cita
    template_name = 'citas/cita_list.html'
    context_object_name = 'citas'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.GET.get('estado', '')
        fecha = self.request.GET.get('fecha', '')
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        if fecha:
            queryset = queryset.filter(fecha__date=fecha)
        
        return queryset.order_by('fecha')

class CitaDetailView(DetailView):
    model = Cita
    template_name = 'citas/cita_detail.html'
    context_object_name = 'cita'

class CitaCreateView(CreateView):
    model = Cita
    form_class = CitaForm
    template_name = 'citas/cita_form.html'
    success_url = reverse_lazy('citas:lista_citas')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cita creada exitosamente.')
        return super().form_valid(form)

class CitaUpdateView(UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = 'citas/cita_form.html'
    context_object_name = 'cita'
    success_url = reverse_lazy('citas:lista_citas')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cita actualizada exitosamente.')
        return super().form_valid(form)

class CitaDeleteView(DeleteView):
    model = Cita
    template_name = 'citas/cita_confirm_delete.html'
    success_url = reverse_lazy('citas:lista_citas')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cita eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

def cambiar_estado_cita(request, pk, estado):
    cita = get_object_or_404(Cita, pk=pk)
    cita.estado = estado
    cita.save()
    
    estados = {
        'confirmada': 'confirmada',
        'completada': 'completada',
        'cancelada': 'cancelada'
    }
    
    if estado in estados:
        messages.success(request, f'Cita {estados[estado]} exitosamente.')
    
    return redirect('citas:detalle_cita', pk=pk)

def citas_hoy(request):
    hoy = timezone.now().date()
    citas = Cita.objects.filter(fecha__date=hoy).order_by('fecha')
    
    return render(request, 'citas/citas_hoy.html', {
        'citas': citas,
        'hoy': hoy
    })