from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:cita_id>/', views.show, name='show'),
    path('<int:cita_id>/edit/', views.edit, name='edit'),
    path('<int:cita_id>/destroy/', views.destroy, name='destroy'),
    path('search/', views.search, name='search'),
    path('hoy/', views.citas_hoy, name='hoy'),
    path('<int:cita_id>/estado/<int:estado_id>/', views.cambiar_estado, name='cambiar_estado'),
]