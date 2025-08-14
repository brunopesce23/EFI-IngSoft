from django.db import migrations
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from datetime import timedelta, date
from decimal import Decimal
from uuid import uuid4
import random


def res_code():
    return uuid4().hex[:8].upper()


def bar_code():
    return f"BOL{uuid4().hex[:12].upper()}"


def crear_asientos(Asiento, avion, filas, columnas):
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    bulk = []
    for f in range(1, filas + 1):
        for c in range(columnas):
            numero = f"{f}{letras[c]}"
            if not Asiento.objects.filter(avion_id=avion.id, numero=numero).exists():
                bulk.append(Asiento(avion_id=avion.id, numero=numero, fila=f, columna=letras[c], tipo="economica", estado="disponible"))
    if bulk:
        Asiento.objects.bulk_create(bulk, ignore_conflicts=True)


def cargar_datos(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    Avion = apps.get_model("gestion_vuelos", "Avion")
    Asiento = apps.get_model("gestion_vuelos", "Asiento")
    Vuelo = apps.get_model("gestion_vuelos", "Vuelo")
    Pasajero = apps.get_model("gestion_vuelos", "Pasajero")
    Reserva = apps.get_model("gestion_vuelos", "Reserva")
    Boleto = apps.get_model("gestion_vuelos", "Boleto")
    PerfilUsuario = apps.get_model("gestion_vuelos", "PerfilUsuario")
    Paquete = apps.get_model("gestion_vuelos", "Paquete")

    # ----------------- Grupos y permisos -----------------
    admin_group, _ = Group.objects.get_or_create(name="admin_app")
    public_group, _ = Group.objects.get_or_create(name="publico")
    app_perms = Permission.objects.filter(content_type__app_label="gestion_vuelos")
    admin_group.permissions.set(list(app_perms))
    public_codes = {"view_vuelo", "view_reserva", "add_reserva"}
    public_group.permissions.set([p for p in app_perms if p.codename in public_codes])

    # ----------------- Usuario admin -----------------
    admin_user, _ = User.objects.get_or_create(
        username="admin",
        defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True, "first_name": "Admin", "last_name": "Aero"},
    )
    admin_user.password = make_password("admin123")
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    admin_user.groups.add(admin_group)
    PerfilUsuario.objects.get_or_create(user_id=admin_user.id, defaults={"rol": "admin"})

    # ----------------- Aviones + Asientos -----------------
    aviones_def = [
        ("Boeing 737-800", 20, 6),
        ("Airbus A320", 22, 6),
        ("Boeing 777-300", 30, 10),
        ("Embraer E190", 18, 4),
        ("Airbus A330-200", 28, 8),
    ]
    aviones = []
    for modelo, filas, columnas in aviones_def:
        avion, _ = Avion.objects.get_or_create(
            modelo=modelo,
            defaults={"capacidad": filas * columnas, "filas": filas, "columnas": columnas},
        )
        if (avion.filas, avion.columnas, avion.capacidad) != (filas, columnas, filas * columnas):
            avion.filas, avion.columnas, avion.capacidad = filas, columnas, filas * columnas
            avion.save()
        crear_asientos(Asiento, avion, filas, columnas)
        aviones.append(avion)

    # ----------------- Vuelos -----------------
    now = timezone.now()

    rutas_nac = [
        ("Buenos Aires", "Córdoba"), ("Córdoba", "Mendoza"), ("Mendoza", "Salta"), ("Salta", "Buenos Aires"),
        ("Buenos Aires", "Bariloche"), ("Bariloche", "Córdoba"), ("Córdoba", "Iguazú"), ("Iguazú", "Buenos Aires"),
        ("Rosario", "Neuquén"), ("Neuquén", "Buenos Aires"), ("Buenos Aires", "Ushuaia"), ("Ushuaia", "Córdoba"),
        ("Córdoba", "Tucumán"), ("Tucumán", "Buenos Aires"), ("Buenos Aires", "Comodoro Rivadavia"), ("Comodoro Rivadavia", "Córdoba"),
        ("Córdoba", "Posadas"), ("Posadas", "Buenos Aires"), ("Buenos Aires", "Bahía Blanca"), ("Bahía Blanca", "Córdoba"),
    ]
    dur_nac = [1.2,1.5,2.0,2.2,2.5,1.7,2.0,1.8,2.1,1.6,3.3,3.0,1.4,1.8,2.6,2.0,1.7,1.9,1.5,1.6]
    from decimal import Decimal as D
    precio_nac = [D("39999.00"),D("45999.00"),D("50999.00"),D("55999.00"),D("62999.00"),
                  D("41999.00"),D("49999.00"),D("48999.00"),D("52999.00"),D("44999.00"),
                  D("89999.00"),D("82999.00"),D("43999.00"),D("49999.00"),D("69999.00"),
                  D("52999.00"),D("46999.00"),D("51999.00"),D("47999.00"),D("48999.00")]

    rutas_int = [
        ("Buenos Aires (EZE)", "Miami (MIA)"), ("Buenos Aires (EZE)", "New York (JFK)"),
        ("Buenos Aires (EZE)", "Madrid (MAD)"), ("Buenos Aires (EZE)", "Barcelona (BCN)"),
        ("Buenos Aires (EZE)", "Paris (CDG)"), ("Buenos Aires (EZE)", "Roma (FCO)"),
        ("Buenos Aires (EZE)", "Londres (LHR)"), ("Buenos Aires (EZE)", "San Pablo (GRU)"),
        ("Buenos Aires (EZE)", "Río de Janeiro (GIG)"), ("Buenos Aires (EZE)", "Tokio (HND)"),
    ]
    dur_int = [9.0,11.0,12.5,12.8,13.0,13.2,14.0,3.0,3.2,28.0]
    precio_int = [D("399999.00"),D("489999.00"),D("549999.00"),D("539999.00"),
                  D("569999.00"),D("549999.00"),D("599999.00"),D("189999.00"),
                  D("199999.00"),D("799999.00")]

    vuelos = []
    # AR001..AR020 nacionales
    for i in range(20):
        codigo = f"AR{(i+1):03d}"
        origen, destino = rutas_nac[i]
        salida = now + timedelta(days=i+1, hours=8 + (i % 5))
        llegada = salida + timedelta(hours=dur_nac[i])
        avion = aviones[i % len(aviones[:-1])]
        vuelo, _ = Vuelo.objects.get_or_create(
            codigo_vuelo=codigo,
            defaults={
                "avion_id": avion.id,
                "origen": origen,
                "destino": destino,
                "fecha_salida": salida,
                "fecha_llegada": llegada,
                "duracion": llegada - salida,
                "estado": "programado",
                "precio_base": precio_nac[i],
            },
        )
        vuelos.append(vuelo)

    # AI101..AI110 internacionales
    for i in range(10):
        codigo = f"AI{101+i}"
        origen, destino = rutas_int[i]
        salida = now + timedelta(days=i+2, hours=20 + (i % 3))
        llegada = salida + timedelta(hours=dur_int[i])
        avion = aviones[2] if i != 9 else aviones[4]  # 777 o A330
        vuelo, _ = Vuelo.objects.get_or_create(
            codigo_vuelo=codigo,
            defaults={
                "avion_id": avion.id,
                "origen": origen,
                "destino": destino,
                "fecha_salida": salida,
                "fecha_llegada": llegada,
                "duracion": llegada - salida,
                "estado": "programado",
                "precio_base": precio_int[i],
            },
        )
        vuelos.append(vuelo)

    # ----------------- Pasajeros base -----------------
    pasajeros_def = [
        ("Juan Carlos", "DNI10000001", "juan.carlos@example.com", "351-111-1111", date(1990, 5, 10)),
        ("María Elena", "DNI10000002", "maria.elena@example.com", "351-222-2222", date(1988, 7, 22)),
        ("Pedro Gómez", "DNI10000003", "pedro.gomez@example.com", "351-333-3333", date(1992, 3, 14)),
        ("Lucía Martínez", "DNI10000004", "lucia.martinez@example.com", "351-444-4444", date(1995, 11, 5)),
        ("Santiago Ruiz", "DNI10000005", "santiago.ruiz@example.com", "351-555-5555", date(1987, 1, 30)),
        ("Carolina Pérez", "DNI10000006", "carolina.perez@example.com", "351-666-6666", date(1993, 9, 18)),
        ("Gonzalo Torres", "DNI10000007", "gonzalo.torres@example.com", "351-777-7777", date(1991, 2, 2)),
        ("Valentina López", "DNI10000008", "valentina.lopez@example.com", "351-888-8888", date(1994, 6, 25)),
        ("Nicolás Fernández", "DNI10000009", "nicolas.fernandez@example.com", "351-999-9999", date(1989, 12, 12)),
        ("Camila Alvarez", "DNI10000010", "camila.alvarez@example.com", "351-123-4567", date(1996, 4, 4)),
    ]
    pasajeros = []
    for nombre, doc, mail, tel, fnac in pasajeros_def:
        p, _ = Pasajero.objects.get_or_create(
            documento=doc,
            defaults={
                "nombre": nombre,
                "tipo_documento": "dni",
                "email": mail,
                "telefono": tel,
                "fecha_nacimiento": fnac,
            },
        )
        pasajeros.append(p)

    # ----------------- Reservas realistas -----------------
    random.seed(42)

    def boleto_para(reserva):
        Boleto.objects.update_or_create(
            reserva_id=reserva.id,
            defaults={"codigo_barra": bar_code(), "estado": "emitido"},
        )

    def ocupar_porcentaje(vuelo, porcentaje):
        asientos = list(Asiento.objects.filter(avion_id=vuelo.avion_id).order_by("fila", "columna"))
        objetivo = max(1, int(len(asientos) * porcentaje))
        ocupadas = 0
        idx = 0
        while ocupadas < objetivo and idx < len(asientos):
            asiento = asientos[idx]
            res, created = Reserva.objects.get_or_create(
                vuelo_id=vuelo.id,
                asiento_id=asiento.id,
                defaults={
                    "pasajero_id": pasajeros[ocupadas % len(pasajeros)].id,
                    "estado": "confirmada",
                    "precio": vuelo.precio_base,
                    "codigo_reserva": res_code(),
                },
            )
            if not created and res.estado not in ("confirmada", "pagada"):
                res.estado = "confirmada"
                res.precio = vuelo.precio_base
                res.save(update_fields=["estado", "precio"])
            asiento.estado = "reservado"
            asiento.save(update_fields=["estado"])
            boleto_para(res)
            ocupadas += 1
            idx += 1

    for v in vuelos:
        dow = v.fecha_salida.weekday()
        es_fin = dow in (5, 6)
        es_int = v.codigo_vuelo.startswith("AI")
        if es_int:
            base = (0.60, 0.90) if not es_fin else (0.75, 0.95)
        else:
            base = (0.35, 0.75) if not es_fin else (0.60, 0.80)
        ocupar_porcentaje(v, random.uniform(*base))

    # ----------------- Paquetes con imágenes -----------------
    paquetes = [
        {"titulo": "Búzios All Inclusive", "destino": "Búzios, Brasil", "descripcion": "7 noches, hotel all inclusive, traslados y asistencia.",
         "precio_desde": Decimal("399999.00"), "duracion_noches": 7, "incluye": "Aéreos, hotel 4*, traslados, seguro médico",
         "imagen_url": "https://images.unsplash.com/photo-1500048993953-d23a436266cf?q=80&w=1400&auto=format&fit=crop"},
        {"titulo": "Río de Janeiro Playero", "destino": "Río de Janeiro, Brasil", "descripcion": "5 noches en Copacabana con desayuno, city tour incluido.",
         "precio_desde": Decimal("359999.00"), "duracion_noches": 5, "incluye": "Aéreos, hotel 3*, desayuno, city tour",
         "imagen_url": "https://images.unsplash.com/photo-1544989164-31dc3c645987?q=80&w=1400&auto=format&fit=crop"},
        {"titulo": "Florianópolis Familiar", "destino": "Florianópolis, Brasil", "descripcion": "7 noches, hotel con piscina, ideal familias.",
         "precio_desde": Decimal("329999.00"), "duracion_noches": 7, "incluye": "Aéreos, hotel 3*, traslados, seguro",
         "imagen_url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1400&auto=format&fit=crop"},
        {"titulo": "Punta Cana Premium", "destino": "Punta Cana, República Dominicana", "descripcion": "7 noches all inclusive 5*, playa paradisíaca.",
         "precio_desde": Decimal("799999.00"), "duracion_noches": 7, "incluye": "Aéreos, hotel 5*, traslados, all inclusive",
         "imagen_url": "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?q=80&w=1400&auto=format&fit=crop"},
        {"titulo": "Cancún Todo Incluido", "destino": "Cancún, México", "descripcion": "6 noches en la zona hotelera, all inclusive.",
         "precio_desde": Decimal("749999.00"), "duracion_noches": 6, "incluye": "Aéreos, hotel 5*, traslados, all inclusive",
         "imagen_url": "https://images.unsplash.com/photo-1506929562872-bb421503ef21?q=80&w=1400&auto=format&fit=crop"},
        {"titulo": "Europa Clásica", "destino": "Madrid - París - Roma", "descripcion": "12 noches recorriendo las capitales clásicas de Europa.",
         "precio_desde": Decimal("1499999.00"), "duracion_noches": 12, "incluye": "Aéreos, hoteles 4*, traslados, city tours",
         "imagen_url": "https://images.unsplash.com/photo-1508057198894-247b23fe5ade?q=80&w=1400&auto=format&fit=crop"},
        {"titulo": "Costa Amalfitana & Roma", "destino": "Italia", "descripcion": "10 noches entre Roma y la Costa Amalfitana.",
         "precio_desde": Decimal("1399999.00"), "duracion_noches": 10, "incluye": "Aéreos, hoteles, traslados y asistencia",
         "imagen_url": "https://images.unsplash.com/photo-1505764706515-aa95265c5abc?q=80&w=1400&auto=format&fit=crop"},
        {"titulo": "USA City Combo", "destino": "Miami & New York, EEUU", "descripcion": "8 noches combinando compras y city-life.",
         "precio_desde": Decimal("1099999.00"), "duracion_noches": 8, "incluye": "Aéreos, hoteles 3/4*, traslados",
         "imagen_url": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=1400&auto=format&fit=crop"},
        {"titulo": "Tokio Discovery", "destino": "Tokio, Japón", "descripcion": "7 noches para descubrir la cultura japonesa.",
         "precio_desde": Decimal("1799999.00"), "duracion_noches": 7, "incluye": "Aéreos, hotel 4*, traslados, asistencia",
         "imagen_url": "https://images.unsplash.com/photo-1518544801976-3e188ee7c3a4?q=80&w=1400&auto=format&fit=crop"},
    ]
    for data in paquetes:
        Paquete.objects.update_or_create(titulo=data["titulo"], defaults=data)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("gestion_vuelos", "0001_tablas"),
    ]

    operations = [
        migrations.RunPython(cargar_datos, reverse_code=noop_reverse),
    ]
