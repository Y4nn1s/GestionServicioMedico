from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pacientes.models import Paciente
from citas.models import Cita
from historiales.models import HistorialMedico
from django.utils import timezone

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