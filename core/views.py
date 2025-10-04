from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.urls import reverse_lazy
from pacientes.models import Paciente
from citas.models import Cita
from historiales.models import HistorialMedico
from .models import PerfilUsuario
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


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('core:dashboard')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('core:dashboard')


class UsuarioCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    template_name = 'registration/usuario_form.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
    success_url = reverse_lazy('core:lista_usuarios')
    
    def test_func(self):
        return self.request.user.perfilusuario.rol == 'admin'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Asignar rol desde el formulario o establecer por defecto
        rol = self.request.POST.get('rol', 'recepcionista')
        
        # Actualizar el rol en el perfil existente
        perfil = self.object.perfilusuario
        perfil.rol = rol
        perfil.save()
        
        # Agregar al grupo correspondiente
        grupo_nombre = rol.capitalize() if rol != 'recepcionista' else 'Recepcionista'
        grupo, created = Group.objects.get_or_create(name=grupo_nombre)
        self.object.groups.add(grupo)
        
        messages.success(self.request, f'Usuario {self.object.username} creado exitosamente.')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = PerfilUsuario.ROL_OPCIONES
        return context


class UsuarioListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'registration/usuario_list.html'
    context_object_name = 'usuarios'
    
    def test_func(self):
        return self.request.user.perfilusuario.rol == 'admin'
    
    def get_queryset(self):
        return User.objects.select_related('perfilusuario').all()


@login_required
def cambiar_rol(request, user_id):
    if request.user.perfilusuario.rol != 'admin':
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('core:dashboard')
    
    usuario = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        nuevo_rol = request.POST.get('rol')
        if nuevo_rol in ['admin', 'medico', 'recepcionista']:
            perfil_usuario = usuario.perfilusuario
            perfil_usuario.rol = nuevo_rol
            perfil_usuario.save()
            
            # Limpiar grupos anteriores
            usuario.groups.clear()
            
            # Agregar al grupo correspondiente
            grupo_nombre = nuevo_rol.capitalize() if nuevo_rol != 'recepcionista' else 'Recepcionista'
            grupo, created = Group.objects.get_or_create(name=grupo_nombre)
            usuario.groups.add(grupo)
            
            messages.success(request, f'Rol de {usuario.username} actualizado a {nuevo_rol}.')
        else:
            messages.error(request, 'Rol no válido.')
        
        return redirect('core:lista_usuarios')
    
    context = {
        'usuario': usuario,
        'roles': PerfilUsuario.ROL_OPCIONES
    }
    return render(request, 'registration/cambiar_rol.html', context)