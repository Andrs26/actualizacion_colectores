# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Cliente, ClienteDatos, ClienteContacto

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente, ClienteDatos, ClienteContacto
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

@login_required
def asignacion_usuario(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    tab = request.GET.get('tab', 'pendientes')
    busqueda = request.GET.get('q', '')

    base_filter = Q(usuario_asignado=request.user)
    if tab == 'pendientes':
        base_filter &= Q(estado='Pendiente')
    elif tab == 'actualizados':
        base_filter &= Q(estado='Actualizado')
    elif tab == 'no_ubicados':
        base_filter &= Q(estado='No Ubicado')
    else:
        base_filter &= Q(pk__in=[])

    if busqueda:
        base_filter &= Q(nombre_empresa__icontains=busqueda)

    clientes_qs = Cliente.objects.filter(base_filter)

    paginator = Paginator(clientes_qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'is_admin': request.user.is_superuser or 'admin' in user_groups,
        'is_colector': 'colector' in user_groups,
        'page_obj': page_obj,
        'tab': tab,
        'q': busqueda,
    }

    return render(request, 'actualizacion/asignacion_usuario.html', context)

@login_required
def detalle_cliente(request, cliente_id):
    user_groups = request.user.groups.values_list('name', flat=True)
    cliente = Cliente.objects.get(id=cliente_id, usuario_asignado=request.user)
    datos = getattr(cliente, 'datos', None)
    contactos = cliente.contactos.all()

    # Agregar conteos para el usuario asignado
    procesados_count = Cliente.objects.filter(usuario_asignado=request.user, estado__in=['Actualizado', 'No Ubicado']).count()
    pendientes_count = Cliente.objects.filter(usuario_asignado=request.user, estado='Pendiente').count()
    asignados_count = Cliente.objects.filter(usuario_asignado=request.user).count()

    return render(request, 'actualizacion/detalle_cliente.html', {
        'cliente': cliente,
        'datos': datos,
        'contactos': contactos,
        'is_admin': request.user.is_superuser or 'admin' in user_groups,
        'is_colector': 'colector' in user_groups,
        'procesados_count': procesados_count,
        'pendientes_count': pendientes_count,
        'asignados_count': asignados_count,
    })

@login_required
def ver_detalle_cliente(request, cliente_id):
    user_groups = request.user.groups.values_list('name', flat=True)
    cliente = Cliente.objects.get(id=cliente_id, usuario_asignado=request.user)
    datos = getattr(cliente, 'datos', None)
    contactos = cliente.contactos.all()
    
    return render(request, 'actualizacion/ver_detalle_cliente.html', {
        'cliente': cliente,
        'datos': datos,
        'contactos': contactos,
        'is_admin': request.user.is_superuser or 'admin' in user_groups,
        'is_colector': 'colector' in user_groups,
    })

# Agrega la función de actualización del cliente
from django.contrib import messages

@login_required
def actualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        cliente.estado = 'Actualizado'
        cliente.observaciones = request.POST.get('observaciones', cliente.observaciones)
        cliente.save()

        datos = getattr(cliente, 'datos', None)
        if datos:
            datos.direccion = request.POST.get('direccion', datos.direccion)
            datos.telefono = request.POST.get('telefono', datos.telefono)
            datos.correo = request.POST.get('correo', datos.correo)
            datos.pagina_web = request.POST.get('pagina_web', datos.pagina_web)
            datos.numero_sucursales = request.POST.get('numero_sucursales', datos.numero_sucursales)
            datos.numero_empleados = request.POST.get('numero_empleados', datos.numero_empleados)
            datos.principales_productos = request.POST.get('productos_servicios', datos.principales_productos)
            datos.save()

        # Guardar contactos (máximo 4)
        contactos = cliente.contactos.all()
        total_contactos = 4  # Asumimos 4 contactos como máximo

        for i in range(total_contactos):
            nombre = request.POST.get(f'nombre_{i}', '')
            apellido = request.POST.get(f'apellido_{i}', '')
            telefono = request.POST.get(f'telefono_{i}', '')
            correo = request.POST.get(f'correo_{i}', '')
            cargo = request.POST.get(f'cargo_{i}', '')

            if nombre and apellido:
                if i < contactos.count():
                    c = contactos[i]
                else:
                    c = ClienteContacto(cliente=cliente)
                c.nombre = nombre
                c.apellido = apellido
                c.telefono = telefono
                c.correo = correo
                c.cargo = cargo
                c.save()

        messages.success(request, "Datos actualizados correctamente.")
        return redirect('ver_detalle_cliente', cliente_id=cliente.id)

# Nueva función: marcar_no_ubicado
from django.contrib import messages

@login_required
def marcar_no_ubicado(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.estado = "No Ubicado"
    cliente.save()
    messages.warning(request, "El cliente se ha marcado como No Ubicado.")
    return redirect('ver_detalle_cliente', cliente_id=cliente.id)

# Nueva función para editar cliente
from django.shortcuts import get_object_or_404

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id, usuario_asignado=request.user)
    datos = getattr(cliente, 'datos', None)
    contactos = cliente.contactos.all()

    if request.method == 'POST':
        cliente.nombre_empresa = request.POST.get('nombre_empresa', cliente.nombre_empresa)
        cliente.estado = request.POST.get('estado', cliente.estado)
        cliente.observaciones = request.POST.get('observaciones', cliente.observaciones)
        cliente.save()

        if datos:
            datos.direccion = request.POST.get('direccion', datos.direccion)
            datos.telefono = request.POST.get('telefono', datos.telefono)
            datos.correo = request.POST.get('correo', datos.correo)
            datos.pagina_web = request.POST.get('pagina_web', datos.pagina_web)
            datos.numero_sucursales = request.POST.get('numero_sucursales') or datos.numero_sucursales
            datos.numero_empleados = request.POST.get('numero_empleados') or datos.numero_empleados
            datos.principales_productos = request.POST.get('principales_productos', datos.principales_productos)
            datos.save()

        # Actualiza cada contacto individualmente (requiere manejar múltiples entradas si existen varios)
        for contacto in contactos:
            contacto.nombre = request.POST.get(f'nombre_{contacto.id}', contacto.nombre)
            contacto.apellido = request.POST.get(f'apellido_{contacto.id}', contacto.apellido)
            contacto.telefono = request.POST.get(f'telefono_{contacto.id}', contacto.telefono)
            contacto.correo = request.POST.get(f'correo_{contacto.id}', contacto.correo)
            contacto.cargo = request.POST.get(f'cargo_{contacto.id}', contacto.cargo)
            contacto.save()

        return redirect('detalle_cliente', cliente_id=cliente.id)

    return render(request, 'actualizacion/editar_cliente.html', {
        'cliente': cliente,
        'datos': datos,
        'contactos': contactos
    })
