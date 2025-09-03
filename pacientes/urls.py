from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('store/', views.create, name='store'),  # Redirigir a create para manejo POST
    path('<int:paciente_id>/', views.show, name='show'),
    path('<int:paciente_id>/edit/', views.edit, name='edit'),
    path('<int:paciente_id>/update/', views.edit, name='update'),  # Redirigir a edit para manejo POST
    path('<int:paciente_id>/destroy/', views.destroy, name='destroy'),
]