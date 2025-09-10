from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Paciente
from .forms import PacienteForm

class PacienteListView(ListView):
    model = Paciente
    template_name = 'pacientes/paciente_list.html'
    context_object_name = 'pacientes'
    paginate_by = 10

class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'pacientes/paciente_detail.html'
    context_object_name = 'paciente'

class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/paciente_form.html'
    success_url = reverse_lazy('pacientes:lista_pacientes')
    
    def form_valid(self, form):
        messages.success(self.request, 'Paciente creado exitosamente.')
        return super().form_valid(form)

class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/paciente_form.html'
    context_object_name = 'paciente'
    success_url = reverse_lazy('pacientes:lista_pacientes')
    
    def form_valid(self, form):
        messages.success(self.request, 'Paciente actualizado exitosamente.')
        return super().form_valid(form)

class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'pacientes/paciente_confirm_delete.html'
    success_url = reverse_lazy('pacientes:lista_pacientes')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Paciente eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

def buscar_pacientes(request):
    query = request.GET.get('q', '')
    pacientes = Paciente.objects.all()
    
    if query:
        pacientes = pacientes.filter(
            models.Q(nombre__icontains=query) |
            models.Q(apellido__icontains=query) |
            models.Q(cedula__icontains=query)
        )
    
    return render(request, 'pacientes/buscar_pacientes.html', {
        'pacientes': pacientes,
        'query': query
    })