from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import timedelta
from .models import Vuelo, Pasajero, Reserva, Asiento, Boleto, Avion, PerfilUsuario, Paquete
from .forms import PasajeroForm, ReservaForm, BusquedaVueloForm


def es_admin(user):
    """Es admin si tiene perfil admin o es staff/superuser."""
    if not user.is_authenticated:
        return False
    try:
        return getattr(user, 'perfil', None) and user.perfil.rol == 'admin' or user.is_staff or user.is_superuser
    except PerfilUsuario.DoesNotExist:
        return user.is_staff or user.is_superuser


def home(request):
    """Página principal: simple para público/cliente, completa para admin"""
    if request.user.is_authenticated and es_admin(request.user):
        total_vuelos = Vuelo.objects.count()
        vuelos_hoy = Vuelo.objects.filter(fecha_salida__date=timezone.now().date()).count()
        total_pasajeros = Pasajero.objects.count()
        reservas_activas = Reserva.objects.filter(estado__in=['confirmada', 'pagada']).count()
        proximos_vuelos = Vuelo.objects.filter(
            fecha_salida__gte=timezone.now()
        ).order_by('fecha_salida')[:10]
    else:
        total_vuelos = Vuelo.objects.filter(
            fecha_salida__gte=timezone.now(),
            estado='programado'
        ).count()
        vuelos_hoy = Vuelo.objects.filter(
            fecha_salida__date=timezone.now().date(),
            estado='programado'
        ).count()
        total_pasajeros = None
        reservas_activas = None
        proximos_vuelos = Vuelo.objects.filter(
            fecha_salida__gte=timezone.now(),
            estado='programado'
        ).order_by('fecha_salida')[:10]
    
    context = {
        'total_vuelos': total_vuelos,
        'vuelos_hoy': vuelos_hoy,
        'total_pasajeros': total_pasajeros,
        'reservas_activas': reservas_activas,
        'proximos_vuelos': proximos_vuelos,
        'es_admin': request.user.is_authenticated and es_admin(request.user),
    }
    return render(request, 'gestion_vuelos/home.html', context)


def registro(request):
    """Registro de nuevos usuarios: quedan como 'cliente'."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            PerfilUsuario.objects.create(user=user, rol='cliente')
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido al sistema.')
            return redirect('gestion_vuelos:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


def lista_vuelos(request):
    """Lista todos los vuelos (público: programados futuros)"""
    if request.user.is_authenticated and es_admin(request.user):
        vuelos = Vuelo.objects.all().order_by('fecha_salida')
    else:
        vuelos = Vuelo.objects.filter(
            fecha_salida__gte=timezone.now(),
            estado='programado'
        ).order_by('fecha_salida')
    paginator = Paginator(vuelos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'gestion_vuelos/lista_vuelos.html', {
        'page_obj': page_obj,
        'es_admin': request.user.is_authenticated and es_admin(request.user)
    })


def detalle_vuelo(request, vuelo_id):
    """Detalle con selector de butacas"""
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    if not (request.user.is_authenticated and es_admin(request.user)) and vuelo.estado != 'programado':
        messages.error(request, 'No tienes permisos para ver este vuelo.')
        return redirect('gestion_vuelos:lista_vuelos')
    
    asientos = vuelo.avion.asientos.all().order_by('fila', 'columna')
    asientos_reservados = Reserva.objects.filter(
        vuelo=vuelo,
        estado__in=['confirmada', 'pagada']
    ).values_list('asiento_id', flat=True)
    
    # Matriz para template
    matriz = {}
    for a in asientos:
        matriz.setdefault(a.fila, {})
        matriz[a.fila][a.columna] = {
            'asiento': a,
            'ocupado': a.id in asientos_reservados,
            'disponible': a.estado == 'disponible' and a.id not in asientos_reservados
        }
    filas_ordenadas = []
    for f in sorted(matriz.keys()):
        cols = [matriz[f][c] for c in sorted(matriz[f].keys())]
        filas_ordenadas.append({'numero': f, 'asientos': cols})
    
    return render(request, 'gestion_vuelos/detalle_vuelo.html', {
        'vuelo': vuelo,
        'filas_asientos': filas_ordenadas,
        'puede_reservar': request.user.is_authenticated and vuelo.estado == 'programado',
        'es_admin': request.user.is_authenticated and es_admin(request.user),
    })


def buscar_vuelos(request):
    """Búsqueda simple con filtros"""
    form = BusquedaVueloForm(request.GET or None)
    vuelos = Vuelo.objects.filter(fecha_salida__gte=timezone.now(), estado='programado')
    if form.is_valid():
        origen = form.cleaned_data.get('origen')
        destino = form.cleaned_data.get('destino')
        fecha_salida = form.cleaned_data.get('fecha_salida')
        if origen:
            vuelos = vuelos.filter(origen__icontains=origen)
        if destino:
            vuelos = vuelos.filter(destino__icontains=destino)
        if fecha_salida:
            vuelos = vuelos.filter(fecha_salida__date=fecha_salida)
    vuelos = vuelos.order_by('fecha_salida')
    paginator = Paginator(vuelos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'gestion_vuelos/buscar_vuelos.html', {'form': form, 'page_obj': page_obj})


@login_required
def crear_reserva(request, vuelo_id):
    """Crear reserva seleccionando asiento"""
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    if vuelo.estado != 'programado':
        messages.error(request, 'No se pueden hacer reservas en este vuelo.')
        return redirect('gestion_vuelos:detalle_vuelo', vuelo_id=vuelo.id)
    if vuelo.esta_lleno:
        messages.error(request, 'Este vuelo está completo.')
        return redirect('gestion_vuelos:detalle_vuelo', vuelo_id=vuelo.id)
    
    if request.method == 'POST':
        asiento_id = request.POST.get('asiento_id')
        if asiento_id:
            try:
                asiento = Asiento.objects.get(id=asiento_id, avion=vuelo.avion)
                # Ocupado?
                if Reserva.objects.filter(vuelo=vuelo, asiento=asiento, estado__in=['confirmada', 'pagada']).exists():
                    messages.error(request, 'Este asiento ya está reservado.')
                    return redirect('gestion_vuelos:crear_reserva', vuelo_id=vuelo.id)
                # Pasajero del user (si no existe lo creamos minimal)
                pasajero, _ = Pasajero.objects.get_or_create(
                    email=request.user.email or f"user{request.user.id}@example.com",
                    defaults={
                        'nombre': request.user.get_full_name() or request.user.username,
                        'documento': f'USER_{request.user.id}',
                        'tipo_documento': 'dni',
                        'telefono': '',
                        'fecha_nacimiento': timezone.now().date(),
                    }
                )
                # Crear reserva
                reserva = Reserva.objects.create(
                    vuelo=vuelo,
                    pasajero=pasajero,
                    asiento=asiento,
                    precio=vuelo.precio_base,
                    estado='confirmada'
                )
                messages.success(request, f'Reserva creada. Código: {reserva.codigo_reserva}')
                return redirect('gestion_vuelos:detalle_reserva', reserva_id=reserva.id)
            except Asiento.DoesNotExist:
                messages.error(request, 'Asiento no válido.')
        else:
            messages.error(request, 'Debe seleccionar un asiento.')
    
    # Preparar matriz de asientos
    asientos = vuelo.avion.asientos.all().order_by('fila', 'columna')
    asientos_reservados = Reserva.objects.filter(vuelo=vuelo, estado__in=['confirmada', 'pagada']).values_list('asiento_id', flat=True)
    matriz = {}
    for a in asientos:
        matriz.setdefault(a.fila, {})
        matriz[a.fila][a.columna] = {
            'asiento': a,
            'ocupado': a.id in asientos_reservados,
            'disponible': a.estado == 'disponible' and a.id not in asientos_reservados
        }
    filas_ordenadas = []
    for f in sorted(matriz.keys()):
        cols = [matriz[f][c] for c in sorted(matriz[f].keys())]
        filas_ordenadas.append({'numero': f, 'asientos': cols})
    return render(request, 'gestion_vuelos/crear_reserva.html', {'vuelo': vuelo, 'filas_asientos': filas_ordenadas})


@login_required
def mis_reservas(request):
    """Reservas del usuario (si tiene pasajero asociado por email)"""
    try:
        pasajero = Pasajero.objects.get(email=request.user.email)
        reservas = pasajero.reservas.all().order_by('-fecha_reserva')
    except Pasajero.DoesNotExist:
        reservas = Reserva.objects.none()
        messages.info(request, 'No tienes reservas registradas aún.')
    paginator = Paginator(reservas, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'gestion_vuelos/mis_reservas.html', {'page_obj': page_obj})


def detalle_reserva(request, reserva_id):
    """Detalle de una reserva"""
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'gestion_vuelos/detalle_reserva.html', {'reserva': reserva})


@login_required
def cancelar_reserva(request, reserva_id):
    """Cancelar una reserva"""
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        reserva.estado = 'cancelada'
        reserva.save()
        messages.success(request, 'Reserva cancelada exitosamente.')
        return redirect('gestion_vuelos:mis_reservas')
    return render(request, 'gestion_vuelos/cancelar_reserva.html', {'reserva': reserva})


@user_passes_test(es_admin)
def lista_pasajeros(request):
    """Lista de pasajeros (admin)"""
    pasajeros = Pasajero.objects.all().order_by('nombre')
    q = request.GET.get('q')
    if q:
        pasajeros = pasajeros.filter(
            Q(nombre__icontains=q) | Q(documento__icontains=q) | Q(email__icontains=q)
        )
    paginator = Paginator(pasajeros, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'gestion_vuelos/lista_pasajeros.html', {'page_obj': page_obj, 'query': q})


@user_passes_test(es_admin)
def reportes(request):
    """Reportes (admin)"""
    total_vuelos = Vuelo.objects.count()
    total_reservas = Reserva.objects.count()
    total_pasajeros = Pasajero.objects.count()
    vuelos_por_estado = Vuelo.objects.values('estado').annotate(count=Count('id'))
    reservas_por_estado = Reserva.objects.values('estado').annotate(count=Count('id'))
    vuelos_proximos = Vuelo.objects.filter(
        fecha_salida__gte=timezone.now(),
        fecha_salida__lte=timezone.now() + timedelta(days=7)
    ).order_by('fecha_salida')
    return render(request, 'gestion_vuelos/reportes.html', {
        'total_vuelos': total_vuelos,
        'total_reservas': total_reservas,
        'total_pasajeros': total_pasajeros,
        'vuelos_por_estado': vuelos_por_estado,
        'reservas_por_estado': reservas_por_estado,
        'vuelos_proximos': vuelos_proximos,
    })


def reporte_vuelo(request, vuelo_id):
    """Reporte detallado de un vuelo (admin o público si programado)"""
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    reservas = vuelo.reservas.filter(estado__in=['confirmada', 'pagada']).order_by('asiento__fila', 'asiento__columna')
    return render(request, 'gestion_vuelos/reporte_vuelo.html', {
        'vuelo': vuelo,
        'reservas': reservas,
        'total_pasajeros': reservas.count(),
        'ingresos_totales': sum(r.precio for r in reservas),
    })


def ver_boleto(request, boleto_id):
    """Mostrar boleto"""
    boleto = get_object_or_404(Boleto, id=boleto_id)
    return render(request, 'gestion_vuelos/ver_boleto.html', {'boleto': boleto})


@login_required
def generar_boleto(request, reserva_id):
    """Generar boleto si no existe"""
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if reserva.estado not in ['confirmada', 'pagada']:
        messages.error(request, 'Solo se pueden generar boletos para reservas confirmadas o pagadas.')
        return redirect('gestion_vuelos:detalle_reserva', reserva_id=reserva.id)
    boleto, created = Boleto.objects.get_or_create(reserva=reserva)
    if created:
        messages.success(request, 'Boleto generado exitosamente.')
    else:
        messages.info(request, 'El boleto ya existe para esta reserva.')
    return redirect('gestion_vuelos:ver_boleto', boleto_id=boleto.id)


# ----------- NUEVO: Paquetes -----------
def lista_paquetes(request):
    """Listado de paquetes turísticos (visible a todos)"""
    paquetes = Paquete.objects.filter(activo=True).order_by('-creado')
    return render(request, 'gestion_vuelos/paquetes.html', {'paquetes': paquetes})
