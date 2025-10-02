from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pacientes.models import Paciente
from citas.models import Cita
from historiales.models import HistorialMedico
from django.utils import timezone
from django.db.models import Q

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas para el dashboard
        context['total_pacientes'] = Paciente.objects.count()
        context['citas_hoy'] = Cita.objects.filter(
            fecha=timezone.now().date()
        ).count()
        context['citas_pendientes'] = Cita.objects.filter(
            estado__nombre='Pendiente'
        ).count()
        context['total_historiales'] = HistorialMedico.objects.count()
        
        # Últimas citas
        context['ultimas_citas'] = Cita.objects.select_related(
            'paciente', 'estado', 'motivo'
        ).order_by('-fecha')[:5]
        
        # Últimos pacientes
        context['ultimos_pacientes'] = Paciente.objects.order_by('-created_at')[:5]
        
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

class ContactView(TemplateView):
    template_name = 'core/contact.html'

def handler404(request, exception):
    return render(request, 'core/404.html', status=404)

def handler500(request):
    return render(request, 'core/500.html', status=500)


def search_all(request):
    query = request.GET.get('q', '')
    results = {
        'pacientes': [],
        'citas': [],
        'historiales': []
    }
    
    if query:
        # Buscar en pacientes (nombre, apellido, número de documento)
        results['pacientes'] = Paciente.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(numero_documento__icontains=query)
        )
        
        # Buscar en citas (paciente asociado, motivo)
        # Primero obtengo los IDs de pacientes que coinciden
        paciente_ids = Paciente.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query)
        ).values_list('id', flat=True)
        
        results['citas'] = Cita.objects.filter(
            Q(paciente_id__in=paciente_ids) |
            Q(motivo__nombre__icontains=query) |
            Q(motivo__descripcion__icontains=query)
        ).select_related('paciente', 'estado', 'motivo')
        
        # Buscar en historiales (paciente asociado, información médica)
        # Primero obtengo los IDs de pacientes que coinciden
        paciente_ids_historial = Paciente.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query)
        ).values_list('id', flat=True)
        
        results['historiales'] = HistorialMedico.objects.filter(
            Q(paciente_id__in=paciente_ids_historial) |
            Q(alergias__icontains=query) |
            Q(enfermedades_preexistentes__icontains=query) |
            Q(medicamentos_actuales__icontains=query)
        ).select_related('paciente')
    
    # Limitar resultados para evitar páginas muy largas
    results['pacientes'] = results['pacientes'][:10]
    results['citas'] = results['citas'][:10]
    results['historiales'] = results['historiales'][:10]
    
    context = {
        'query': query,
        'results': results,
        'total_results': sum([
            len(results['pacientes']),
            len(results['citas']), 
            len(results['historiales'])
        ])
    }
    
    return render(request, 'core/search_results.html', context)