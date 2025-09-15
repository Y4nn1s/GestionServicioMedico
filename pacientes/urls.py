from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:paciente_id>/', views.show, name='show'),
    path('<int:paciente_id>/edit/', views.edit, name='edit'),
    path('<int:paciente_id>/destroy/', views.destroy, name='destroy'),
    path('search/', views.search, name='search'),
]