"""
Script para crear datos de ejemplo en la base de datos
Ejecutar después de hacer las migraciones
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aerolinea_project.settings')
django.setup()

from django.contrib.auth.models import User
from gestion_vuelos.models import Avion, Vuelo, Pasajero, Reserva, PerfilUsuario


def crear_datos_ejemplo():
    print("Creando datos de ejemplo...")
    
    # Crear usuario administrador
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@aerolinea.com',
            password='admin123'
        )
        PerfilUsuario.objects.create(user=admin_user, rol='admin')
        print("✓ Usuario administrador creado (admin/admin123)")
    
    # Crear usuario empleado
    if not User.objects.filter(username='empleado').exists():
        empleado_user = User.objects.create_user(
            username='empleado',
            email='empleado@aerolinea.com',
            password='empleado123'
        )
        empleado_user.is_staff = True
        empleado_user.save()
        PerfilUsuario.objects.create(user=empleado_user, rol='empleado')
        print("✓ Usuario empleado creado (empleado/empleado123)")
    
    # Crear aviones
    aviones_data = [
        {'modelo': 'Boeing 737-800', 'filas': 30, 'columnas': 6},
        {'modelo': 'Airbus A320', 'filas': 28, 'columnas': 6},
        {'modelo': 'Boeing 777-300', 'filas': 42, 'columnas': 9},
        {'modelo': 'Embraer E190', 'filas': 20, 'columnas': 4},
    ]
    
    aviones = []
    for avion_data in aviones_data:
        avion, created = Avion.objects.get_or_create(
            modelo=avion_data['modelo'],
            defaults=avion_data
        )
        if created:
            print(f"✓ Avión creado: {avion.modelo}")
        aviones.append(avion)
    
    # Crear vuelos
    base_date = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    
    vuelos_data = [
        {
            'codigo_vuelo': 'AR001',
            'origen': 'Buenos Aires',
            'destino': 'Córdoba',
            'fecha_salida': base_date + timedelta(days=1),
            'duracion_horas': 1.5,
            'precio_base': Decimal('15000.00'),
            'avion': aviones[0]
        },
        {
            'codigo_vuelo': 'AR002',
            'origen': 'Córdoba',
            'destino': 'Buenos Aires',
            'fecha_salida': base_date + timedelta(days=1, hours=4),
            'duracion_horas': 1.5,
            'precio_base': Decimal('15000.00'),
            'avion': aviones[0]
        },
        {
            'codigo_vuelo': 'AR003',
            'origen': 'Buenos Aires',
            'destino': 'Mendoza',
            'fecha_salida': base_date + timedelta(days=2),
            'duracion_horas': 2,
            'precio_base': Decimal('18000.00'),
            'avion': aviones[1]
        },
        {
            'codigo_vuelo': 'AR004',
            'origen': 'Buenos Aires',
            'destino': 'Bariloche',
            'fecha_salida': base_date + timedelta(days=3),
            'duracion_horas': 2.5,
            'precio_base': Decimal('22000.00'),
            'avion': aviones[2]
        },
        {
            'codigo_vuelo': 'AR005',
            'origen': 'Buenos Aires',
            'destino': 'Salta',
            'fecha_salida': base_date + timedelta(days=4),
            'duracion_horas': 2.2,
            'precio_base': Decimal('20000.00'),
            'avion': aviones[3]
        },
    ]
    
    vuelos = []
    for vuelo_data in vuelos_data:
        duracion_horas = vuelo_data.pop('duracion_horas')
        fecha_llegada = vuelo_data['fecha_salida'] + timedelta(hours=duracion_horas)
        
        vuelo, created = Vuelo.objects.get_or_create(
            codigo_vuelo=vuelo_data['codigo_vuelo'],
            defaults={
                **vuelo_data,
                'fecha_llegada': fecha_llegada
            }
        )
        if created:
            print(f"✓ Vuelo creado: {vuelo.codigo_vuelo}")
        vuelos.append(vuelo)
    
    # Crear pasajeros
    pasajeros_data = [
        {
            'nombre': 'Juan Carlos Pérez',
            'documento': '12345678',
            'tipo_documento': 'dni',
            'email': 'juan.perez@email.com',
            'telefono': '+54 11 1234-5678',
            'fecha_nacimiento': datetime(1985, 3, 15).date()
        },
        {
            'nombre': 'María Elena González',
            'documento': '87654321',
            'tipo_documento': 'dni',
            'email': 'maria.gonzalez@email.com',
            'telefono': '+54 11 8765-4321',
            'fecha_nacimiento': datetime(1990, 7, 22).date()
        },
        {
            'nombre': 'Carlos Alberto Rodríguez',
            'documento': '11223344',
            'tipo_documento': 'dni',
            'email': 'carlos.rodriguez@email.com',
            'telefono': '+54 11 1122-3344',
            'fecha_nacimiento': datetime(1978, 11, 8).date()
        },
        {
            'nombre': 'Ana Sofía Martínez',
            'documento': 'P12345678',
            'tipo_documento': 'pasaporte',
            'email': 'ana.martinez@email.com',
            'telefono': '+54 11 5566-7788',
            'fecha_nacimiento': datetime(1992, 5, 30).date()
        },
    ]
    
    pasajeros = []
    for pasajero_data in pasajeros_data:
        pasajero, created = Pasajero.objects.get_or_create(
            documento=pasajero_data['documento'],
            defaults=pasajero_data
        )
        if created:
            print(f"✓ Pasajero creado: {pasajero.nombre}")
        pasajeros.append(pasajero)
    
    # Crear algunas reservas de ejemplo
    if vuelos and pasajeros:
        # Reserva 1: Juan en vuelo AR001
        vuelo1 = vuelos[0]  # AR001
        asiento1 = vuelo1.avion.asientos.filter(numero='1A').first()
        if asiento1:
            reserva1, created = Reserva.objects.get_or_create(
                vuelo=vuelo1,
                pasajero=pasajeros[0],
                asiento=asiento1,
                defaults={
                    'estado': 'confirmada',
                    'precio': vuelo1.precio_base
                }
            )
            if created:
                print(f"✓ Reserva creada: {reserva1.codigo_reserva}")
        
        # Reserva 2: María en vuelo AR003
        vuelo2 = vuelos[2]  # AR003
        asiento2 = vuelo2.avion.asientos.filter(numero='2B').first()
        if asiento2:
            reserva2, created = Reserva.objects.get_or_create(
                vuelo=vuelo2,
                pasajero=pasajeros[1],
                asiento=asiento2,
                defaults={
                    'estado': 'pagada',
                    'precio': vuelo2.precio_base
                }
            )
            if created:
                print(f"✓ Reserva creada: {reserva2.codigo_reserva}")
    
    print("\n¡Datos de ejemplo creados exitosamente!")
    print("\nCredenciales de acceso:")
    print("Administrador: admin / admin123")
    print("Empleado: empleado / empleado123")
    print("\nPuedes acceder al panel de administración en: http://localhost:8000/admin/")


if __name__ == '__main__':
    crear_datos_ejemplo()
