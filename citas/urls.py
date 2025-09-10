from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('', views.CitaListView.as_view(), name='lista_citas'),
    path('hoy/', views.citas_hoy, name='citas_hoy'),
    path('<int:pk>/', views.CitaDetailView.as_view(), name='detalle_cita'),
    path('crear/', views.CitaCreateView.as_view(), name='crear_cita'),
    path('<int:pk>/editar/', views.CitaUpdateView.as_view(), name='editar_cita'),
    path('<int:pk>/eliminar/', views.CitaDeleteView.as_view(), name='eliminar_cita'),
    path('<int:pk>/estado/<str:estado>/', views.cambiar_estado_cita, name='cambiar_estado_cita'),
]