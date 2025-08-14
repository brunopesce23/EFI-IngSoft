from django.contrib import admin
from .models import Avion, Asiento, Vuelo, Pasajero, Reserva, Boleto, PerfilUsuario, Paquete


@admin.register(Avion)
class AvionAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'capacidad', 'filas', 'columnas', 'fecha_registro')
    search_fields = ('modelo',)


@admin.register(Asiento)
class AsientoAdmin(admin.ModelAdmin):
    list_display = ('avion', 'numero', 'fila', 'columna', 'tipo', 'estado')
    list_filter = ('avion', 'tipo', 'estado')


@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    list_display = ('codigo_vuelo', 'origen', 'destino', 'fecha_salida', 'estado', 'precio_base', 'avion')
    list_filter = ('estado', 'origen', 'destino')
    search_fields = ('codigo_vuelo', 'origen', 'destino')


@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento', 'email', 'telefono', 'fecha_nacimiento')
    search_fields = ('nombre', 'documento', 'email')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('codigo_reserva', 'vuelo', 'pasajero', 'asiento', 'estado', 'precio', 'fecha_reserva')
    list_filter = ('estado',)
    search_fields = ('codigo_reserva', 'vuelo__codigo_vuelo', 'pasajero__nombre')


@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ('codigo_barra', 'reserva', 'estado', 'fecha_emision')
    list_filter = ('estado',)
    search_fields = ('codigo_barra', 'reserva__codigo_reserva')


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'telefono', 'fecha_nacimiento')
    list_filter = ('rol',)
    search_fields = ('user__username',)


@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'destino', 'precio_desde', 'duracion_noches', 'activo', 'creado')
    list_filter = ('activo', 'destino')
    search_fields = ('titulo', 'destino')
