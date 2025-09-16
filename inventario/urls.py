from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Vista principal
    path('', views.index, name='index'),
    
    # URLs para Categorías
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/<int:categoria_id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:categoria_id>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
    
    # URLs para Proveedores
    path('proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/<int:proveedor_id>/editar/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/<int:proveedor_id>/eliminar/', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    # URLs para Medicamentos
    path('medicamentos/', views.listar_medicamentos, name='listar_medicamentos'),
    path('medicamentos/crear/', views.crear_medicamento, name='crear_medicamento'),
    path('medicamentos/<int:medicamento_id>/editar/', views.editar_medicamento, name='editar_medicamento'),
    path('medicamentos/<int:medicamento_id>/eliminar/', views.eliminar_medicamento, name='eliminar_medicamento'),
    
    # URLs para Inventario
    path('inventario/', views.listar_inventario, name='listar_inventario'),
    path('inventario/crear/', views.crear_inventario, name='crear_inventario'),
    path('inventario/<int:inventario_id>/editar/', views.editar_inventario, name='editar_inventario'),
    path('inventario/<int:inventario_id>/eliminar/', views.eliminar_inventario, name='eliminar_inventario'),
    
    # URLs para Stock de Medicamentos
    path('stock/', views.stock_medicamentos, name='stock_medicamentos'),
    
    # URLs para Movimientos
    path('movimientos/', views.listar_movimientos, name='listar_movimientos'),
]