from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


def es_admin(user):
    """
    Verifica si el usuario es administrador
    """
    return user.is_authenticated and hasattr(user, 'perfilusuario') and user.perfilusuario.rol == 'admin'


def es_medico(user):
    """
    Verifica si el usuario es médico o administrador
    """
    return user.is_authenticated and hasattr(user, 'perfilusuario') and (
        user.perfilusuario.rol == 'medico' or user.perfilusuario.rol == 'admin'
    )


def es_recepcionista(user):
    """
    Verifica si el usuario es recepcionista, médico o administrador
    """
    return user.is_authenticated and hasattr(user, 'perfilusuario') and (
        user.perfilusuario.rol in ['recepcionista', 'medico', 'admin']
    )


def admin_required(view_func):
    """
    Decorador para vistas que requieren rol de administrador
    """
    def _wrapped_view(request, *args, **kwargs):
        if es_admin(request.user):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('core:dashboard')
    return _wrapped_view


def medico_required(view_func):
    """
    Decorador para vistas que requieren rol de médico o superior
    """
    def _wrapped_view(request, *args, **kwargs):
        if es_medico(request.user):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('core:dashboard')
    return _wrapped_view


def recepcionista_required(view_func):
    """
    Decorador para vistas que requieren rol de recepcionista o superior
    """
    def _wrapped_view(request, *args, **kwargs):
        if es_recepcionista(request.user):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('core:dashboard')
    return _wrapped_view


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin para vistas basadas en clases que requieren rol de administrador
    """
    def test_func(self):
        return es_admin(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('core:dashboard')


class MedicoRequiredMixin(UserPassesTestMixin):
    """
    Mixin para vistas basadas en clases que requieren rol de médico o superior
    """
    def test_func(self):
        return es_medico(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('core:dashboard')


class RecepcionistaRequiredMixin(UserPassesTestMixin):
    """
    Mixin para vistas basadas en clases que requieren rol de recepcionista o superior
    """
    def test_func(self):
        return es_recepcionista(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('core:dashboard')