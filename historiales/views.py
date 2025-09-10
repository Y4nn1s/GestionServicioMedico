from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import HistorialMedico
from .forms import HistorialMedicoForm

class HistorialMedicoListView(LoginRequiredMixin, ListView):
    model = HistorialMedico
    template_name = 'historiales/historial_list.html'
    context_object_name = 'historiales'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        paciente_id = self.request.GET.get('paciente', '')
        
        if paciente_id:
            queryset = queryset.filter(paciente__id=paciente_id)
        
        return queryset

class HistorialMedicoDetailView(LoginRequiredMixin, DetailView):
    model = HistorialMedico
    template_name = 'historiales/historial_detail.html'
    context_object_name = 'historial'

class HistorialMedicoCreateView(LoginRequiredMixin, CreateView):
    model = HistorialMedico
    form_class = HistorialMedicoForm
    template_name = 'historiales/historial_form.html'
    
    def get_success_url(self):
        return reverse_lazy('historiales:detalle_historial', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Historial médico creado exitosamente.')
        return super().form_valid(form)

class HistorialMedicoUpdateView(LoginRequiredMixin, UpdateView):
    model = HistorialMedico
    form_class = HistorialMedicoForm
    template_name = 'historiales/historial_form.html'
    context_object_name = 'historial'
    
    def get_success_url(self):
        return reverse_lazy('historiales:detalle_historial', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Historial médico actualizado exitosamente.')
        return super().form_valid(form)

def buscar_historiales(request):
    query = request.GET.get('q', '')
    historiales = HistorialMedico.objects.all()
    
    if query:
        historiales = historiales.filter(
            Q(paciente__nombre__icontains=query) |
            Q(paciente__apellido__icontains=query) |
            Q(diagnostico__icontains=query) |
            Q(tratamiento__icontains=query)
        )
    
    return render(request, 'historiales/buscar_historiales.html', {
        'historiales': historiales,
        'query': query
    })