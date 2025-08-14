# gestion_vuelos/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from datetime import datetime


class Avion(models.Model):
    """Modelo para representar un avión de la flota"""
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    capacidad = models.PositiveIntegerField(verbose_name="Capacidad total")
    filas = models.PositiveIntegerField(verbose_name="Número de filas")
    columnas = models.PositiveIntegerField(verbose_name="Asientos por fila")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Avión"
        verbose_name_plural = "Aviones"
        
    def __str__(self):
        return f"{self.modelo} - Capacidad: {self.capacidad}"
    
    def save(self, *args, **kwargs):
        # Calcular capacidad automáticamente
        if self.filas and self.columnas:
            self.capacidad = self.filas * self.columnas
        super().save(*args, **kwargs)


class Vuelo(models.Model):
    """Modelo para representar un vuelo"""
    ESTADOS_VUELO = [
        ('programado', 'Programado'),
        ('abordando', 'Abordando'),
        ('en_vuelo', 'En Vuelo'),
        ('aterrizado', 'Aterrizado'),
        ('cancelado', 'Cancelado'),
        ('retrasado', 'Retrasado'),
    ]
    
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name='vuelos')
    origen = models.CharField(max_length=100, verbose_name="Ciudad de origen")
    destino = models.CharField(max_length=100, verbose_name="Ciudad de destino")
    fecha_salida = models.DateTimeField(verbose_name="Fecha y hora de salida")
    fecha_llegada = models.DateTimeField(verbose_name="Fecha y hora de llegada")
    duracion = models.DurationField(verbose_name="Duración del vuelo", blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_VUELO, default='programado')
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio base")
    codigo_vuelo = models.CharField(max_length=10, unique=True, verbose_name="Código de vuelo")
    
    class Meta:
        verbose_name = "Vuelo"
        verbose_name_plural = "Vuelos"
        ordering = ['fecha_salida']
        
    def __str__(self):
        return f"{self.codigo_vuelo} - {self.origen} → {self.destino}"
    
    def save(self, *args, **kwargs):
        # Calcular duración automáticamente
        if self.fecha_salida and self.fecha_llegada:
            self.duracion = self.fecha_llegada - self.fecha_salida
        super().save(*args, **kwargs)
            # ¿Es un vuelo dentro de Argentina?
    def es_domestico_ar(self) -> bool:
        return _es_argentina(self.origen) and _es_argentina(self.destino)

    # Etiqueta de moneda para mostrar: 'ARS $' o 'USD '
    def etiqueta_moneda(self) -> str:
        return "ARS $" if self.es_domestico_ar() else "USD "

    # Texto listo para mostrar, p.ej. "USD 499.99" o "ARS $ 120000.00"
    def precio_display(self) -> str:
        return f"{self.etiqueta_moneda()}{self.precio_base}"

    
    
    @property
    def asientos_disponibles(self):
        """Retorna el número de asientos disponibles"""
        total_asientos = self.avion.capacidad
        asientos_reservados = self.reservas.filter(estado__in=['confirmada', 'pagada']).count()
        return total_asientos - asientos_reservados
    
    @property
    def esta_lleno(self):
        """Verifica si el vuelo está lleno"""
        return self.asientos_disponibles <= 0

# --- helpers para moneda/país en Vuelo (NO requieren migraciones) ---

# Lista simple de ciudades/provincias de Argentina que usamos en los seeds y pantallas.
# Si en tus datos usás "Buenos Aires (EZE)" o similares, también matchea por prefijo.
AR_CIUDADES = {
    "buenos aires", "eze", "ezeiza", "cordoba", "córdoba", "mdz", "mendoza", "rosario",
    "salta", "neuquen", "neuquén", "bariloche", "ushuaia", "iguazu", "iguazú",
    "mar del plata", "tucuman", "tucumán", "san juan", "san luis", "posadas", "resistencia",
    "bahia blanca", "bahía blanca", "comodoro rivadavia", "trelew"
}

def _es_argentina(texto: str) -> bool:
    if not texto:
        return False
    t = texto.strip().lower()
    # limpiar cosas como "Buenos Aires (EZE)" -> "buenos aires"
    if "(" in t:
        t = t.split("(")[0].strip()
    return any(ciudad in t for ciudad in AR_CIUDADES) or "argentina" in t


class Pasajero(models.Model):
    """Modelo para representar un pasajero"""
    TIPOS_DOCUMENTO = [
        ('dni', 'DNI'),
        ('pasaporte', 'Pasaporte'),
        ('cedula', 'Cédula'),
    ]
    
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    documento = models.CharField(max_length=20, unique=True, verbose_name="Número de documento")
    tipo_documento = models.CharField(max_length=10, choices=TIPOS_DOCUMENTO, default='dni')
    email = models.EmailField(verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Pasajero"
        verbose_name_plural = "Pasajeros"
        
    def __str__(self):
        return f"{self.nombre} - {self.documento}"
    
    @property
    def edad(self):
        """Calcula la edad del pasajero"""
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))


class Asiento(models.Model):
    """Modelo para representar un asiento en un avión"""
    TIPOS_ASIENTO = [
        ('economica', 'Clase Económica'),
        ('ejecutiva', 'Clase Ejecutiva'),
        ('primera', 'Primera Clase'),
    ]
    
    ESTADOS_ASIENTO = [
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('ocupado', 'Ocupado'),
        ('mantenimiento', 'En Mantenimiento'),
    ]
    
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name='asientos')
    numero = models.CharField(max_length=10, verbose_name="Número de asiento")
    fila = models.PositiveIntegerField(verbose_name="Fila")
    columna = models.CharField(max_length=1, verbose_name="Columna")
    tipo = models.CharField(max_length=20, choices=TIPOS_ASIENTO, default='economica')  # <<< FIX: max_length
    estado = models.CharField(max_length=20, choices=ESTADOS_ASIENTO, default='disponible')
    
    class Meta:
        verbose_name = "Asiento"
        verbose_name_plural = "Asientos"
        unique_together = ['avion', 'numero']
        ordering = ['fila', 'columna']
        
    def __str__(self):
        return f"{self.avion.modelo} - Asiento {self.numero}"


class Reserva(models.Model):
    """Modelo para representar una reserva de vuelo"""
    ESTADOS_RESERVA = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('pagada', 'Pagada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]
    
    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE, related_name='reservas')
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, related_name='reservas')
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE, related_name='reservas')
    estado = models.CharField(max_length=20, choices=ESTADOS_RESERVA, default='pendiente')
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio final")
    codigo_reserva = models.CharField(max_length=10, unique=True, verbose_name="Código de reserva")
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        unique_together = ['vuelo', 'asiento']  # Un asiento no puede estar reservado más de una vez por vuelo
        ordering = ['-fecha_reserva']
        
    def __str__(self):
        return f"Reserva {self.codigo_reserva} - {self.pasajero.nombre}"
    
    def save(self, *args, **kwargs):
        # Generar código de reserva único si está vacío
        if not self.codigo_reserva:
            self.codigo_reserva = str(uuid.uuid4())[:8].upper()
        # Establecer precio basado en el vuelo si no está seteado
        if not self.precio:
            self.precio = self.vuelo.precio_base
        super().save(*args, **kwargs)
        # Actualizar estado del asiento
        if self.estado in ['confirmada', 'pagada']:
            if self.asiento.estado != 'reservado':
                self.asiento.estado = 'reservado'
                self.asiento.save(update_fields=['estado'])
        elif self.estado == 'cancelada':
            if self.asiento.estado != 'disponible':
                self.asiento.estado = 'disponible'
                self.asiento.save(update_fields=['estado'])


class Boleto(models.Model):
    """Modelo para representar un boleto electrónico"""
    ESTADOS_BOLETO = [
        ('emitido', 'Emitido'),
        ('usado', 'Usado'),
        ('cancelado', 'Cancelado'),
    ]
    
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='boleto')
    codigo_barra = models.CharField(max_length=50, unique=True, verbose_name="Código de barras")
    fecha_emision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_BOLETO, default='emitido')
    
    class Meta:
        verbose_name = "Boleto"
        verbose_name_plural = "Boletos"
        
    def __str__(self):
        return f"Boleto {self.codigo_barra} - {self.reserva.codigo_reserva}"
    
    def save(self, *args, **kwargs):
        # Generar código de barras único si está vacío
        if not self.codigo_barra:
            timestamp = str(int(datetime.now().timestamp()))
            self.codigo_barra = f"BOL{timestamp}{self.reserva.id if self.reserva_id else ''}"
        super().save(*args, **kwargs)


class PerfilUsuario(models.Model):
    """Extensión del modelo User para roles específicos"""
    ROLES = [
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        
    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"


class Paquete(models.Model):
    """Paquetes turísticos para la sección de Paquetes"""
    titulo = models.CharField(max_length=150)
    destino = models.CharField(max_length=120)
    descripcion = models.TextField()
    precio_desde = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_noches = models.PositiveIntegerField(default=7)
    incluye = models.TextField(help_text="Lista o texto con servicios incluidos")
    imagen_url = models.URLField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes"

    def __str__(self):
        return f"{self.titulo} - {self.destino}"
