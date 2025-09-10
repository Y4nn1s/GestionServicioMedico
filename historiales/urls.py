from django.urls import path
from . import views

app_name = 'historiales'

urlpatterns = [
    path('', views.HistorialMedicoListView.as_view(), name='lista_historiales'),
    path('buscar/', views.buscar_historiales, name='buscar_historiales'),
    path('<int:pk>/', views.HistorialMedicoDetailView.as_view(), name='detalle_historial'),
    path('crear/', views.HistorialMedicoCreateView.as_view(), name='crear_historial'),
    path('<int:pk>/editar/', views.HistorialMedicoUpdateView.as_view(), name='editar_historial'),
]