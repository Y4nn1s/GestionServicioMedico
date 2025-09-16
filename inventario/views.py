from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Categoria, Proveedor, Medicamento, Inventario, MovimientoInventario
from .forms import CategoriaForm, ProveedorForm, MedicamentoForm, InventarioForm

# Vistas para Categorías
def listar_categorias(request):
    categorias_list = Categoria.objects.all()
    paginator = Paginator(categorias_list, 10)
    page_number = request.GET.get('page')
    categorias = paginator.get_page(page_number)
    return render(request, 'inventario/categorias/listar.html', {'categorias': categorias})

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('inventario:listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'inventario/categorias/formulario.html', {'form': form, 'titulo': 'Crear Categoría'})

def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('inventario:listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'inventario/categorias/formulario.html', {'form': form, 'titulo': 'Editar Categoría'})

def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('inventario:listar_categorias')
    return render(request, 'inventario/categorias/eliminar.html', {'categoria': categoria})

# Vistas para Proveedores
def listar_proveedores(request):
    proveedores_list = Proveedor.objects.all()
    paginator = Paginator(proveedores_list, 10)
    page_number = request.GET.get('page')
    proveedores = paginator.get_page(page_number)
    return render(request, 'inventario/proveedores/listar.html', {'proveedores': proveedores})

def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado exitosamente.')
            return redirect('inventario:listar_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'inventario/proveedores/formulario.html', {'form': form, 'titulo': 'Crear Proveedor'})

def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado exitosamente.')
            return redirect('inventario:listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'inventario/proveedores/formulario.html', {'form': form, 'titulo': 'Editar Proveedor'})

def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado exitosamente.')
        return redirect('inventario:listar_proveedores')
    return render(request, 'inventario/proveedores/eliminar.html', {'proveedor': proveedor})

# Vistas para Medicamentos
def listar_medicamentos(request):
    medicamentos_list = Medicamento.objects.select_related('categoria', 'proveedor').all()
    paginator = Paginator(medicamentos_list, 10)
    page_number = request.GET.get('page')
    medicamentos = paginator.get_page(page_number)
    return render(request, 'inventario/medicamentos/listar.html', {'medicamentos': medicamentos})

def crear_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            # El código se generará automáticamente en el modelo
            medicamento = form.save(commit=False)
            medicamento.save()
            messages.success(request, 'Medicamento creado exitosamente.')
            return redirect('inventario:listar_medicamentos')
    else:
        form = MedicamentoForm()
    return render(request, 'inventario/medicamentos/formulario.html', {'form': form, 'titulo': 'Crear Medicamento'})

def editar_medicamento(request, medicamento_id):
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicamento actualizado exitosamente.')
            return redirect('inventario:listar_medicamentos')
    else:
        form = MedicamentoForm(instance=medicamento)
    return render(request, 'inventario/medicamentos/formulario.html', {'form': form, 'titulo': 'Editar Medicamento'})

def eliminar_medicamento(request, medicamento_id):
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
    if request.method == 'POST':
        medicamento.delete()
        messages.success(request, 'Medicamento eliminado exitosamente.')
        return redirect('inventario:listar_medicamentos')
    return render(request, 'inventario/medicamentos/eliminar.html', {'medicamento': medicamento})

# Vistas para Inventario
def listar_inventario(request):
    inventario_list = Inventario.objects.select_related('medicamento').all()
    paginator = Paginator(inventario_list, 10)
    page_number = request.GET.get('page')
    inventario = paginator.get_page(page_number)
    return render(request, 'inventario/inventario/listar.html', {
        'inventario': inventario,
        'today': timezone.now().date()
    })

def crear_inventario(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Existencia de inventario creada exitosamente.')
            return redirect('inventario:listar_inventario')
    else:
        form = InventarioForm()
    return render(request, 'inventario/inventario/formulario.html', {'form': form, 'titulo': 'Agregar Existencia'})

def editar_inventario(request, inventario_id):
    inventario = get_object_or_404(Inventario, id=inventario_id)
    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=inventario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Existencia de inventario actualizada exitosamente.')
            return redirect('inventario:listar_inventario')
    else:
        form = InventarioForm(instance=inventario)
    return render(request, 'inventario/inventario/formulario.html', {'form': form, 'titulo': 'Editar Existencia'})

def eliminar_inventario(request, inventario_id):
    inventario = get_object_or_404(Inventario, id=inventario_id)
    if request.method == 'POST':
        inventario.delete()
        messages.success(request, 'Existencia de inventario eliminada exitosamente.')
        return redirect('inventario:listar_inventario')
    return render(request, 'inventario/inventario/eliminar.html', {'inventario': inventario})

# Vista para mostrar stock total por medicamento
def stock_medicamentos(request):
    # Obtener todos los medicamentos con su stock actual
    medicamentos_list = Medicamento.objects.select_related('categoria', 'proveedor').all()
    for medicamento in medicamentos_list:
        medicamento.stock = medicamento.stock_actual
        medicamento.estado = medicamento.estado_stock
    
    paginator = Paginator(medicamentos_list, 10)
    page_number = request.GET.get('page')
    medicamentos = paginator.get_page(page_number)
    
    return render(request, 'inventario/stock_medicamentos.html', {'medicamentos': medicamentos})

# Vistas para Movimientos
def listar_movimientos(request):
    movimientos_list = MovimientoInventario.objects.select_related('medicamento').all()
    paginator = Paginator(movimientos_list, 10)
    page_number = request.GET.get('page')
    movimientos = paginator.get_page(page_number)
    return render(request, 'inventario/movimientos/listar.html', {'movimientos': movimientos})

# Vista principal del inventario
def index(request):
    return render(request, 'inventario/index.html')