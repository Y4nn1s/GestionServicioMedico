from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('', views.PacienteListView.as_view(), name='lista_pacientes'),
    path('buscar/', views.buscar_pacientes, name='buscar_pacientes'),
    path('<int:pk>/', views.PacienteDetailView.as_view(), name='detalle_paciente'),
    path('crear/', views.PacienteCreateView.as_view(), name='crear_paciente'),
    path('<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='editar_paciente'),
    path('<int:pk>/eliminar/', views.PacienteDeleteView.as_view(), name='eliminar_paciente'),
]