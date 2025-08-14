# Sistema de Gestión de Aerolínea

Sistema web completo desarrollado en Django para la gestión integral de una aerolínea, incluyendo vuelos, reservas, pasajeros y reportes.

## Características Principales

### Funcionalidades Implementadas

1. **Gestión de Vuelos**
   - Crear, editar y eliminar vuelos desde el panel de administración
   - Visualización de vuelos disponibles para usuarios
   - Información completa: origen, destino, fechas, duración, precios
   - Asignación automática de aviones a vuelos

2. **Gestión de Pasajeros**
   - Registro completo de pasajeros con validaciones
   - Información personal: nombre, documento, contacto, fecha de nacimiento
   - Historial completo de vuelos por pasajero
   - Validación de documentos únicos

3. **Sistema de Reservas**
   - Visualización de disponibilidad de asientos en tiempo real
   - Reserva de asientos específicos con mapa visual
   - Gestión de estados: disponible, reservado, ocupado
   - Códigos de reserva únicos generados automáticamente
   - Validaciones para evitar dobles reservas

4. **Gestión de Aviones**
   - Registro completo de la flota
   - Definición automática de layout de asientos
   - Información técnica: modelo, capacidad, configuración
   - Creación automática de asientos basada en filas y columnas

5. **Sistema de Boletos Electrónicos**
   - Generación automática de boletos para reservas confirmadas
   - Códigos de barras únicos
   - Estados de boletos: emitido, usado, cancelado

6. **Reportes y Estadísticas**
   - Dashboard con estadísticas generales
   - Listado detallado de pasajeros por vuelo
   - Reportes de ocupación y ingresos
   - Filtros y búsquedas avanzadas

7. **Sistema de Autenticación**
   - Registro e inicio de sesión de usuarios
   - Roles diferenciados: administrador, empleado, cliente
   - Perfiles de usuario extendidos
   - Protección de rutas según permisos

## Tecnologías Utilizadas

- **Backend**: Django 4.2.7
- **Base de Datos**: SQLite (local)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: Vanilla JS para interactividad
- **Iconos**: Font Awesome 6

## Estructura del Proyecto

\`\`\`
aerolinea_project/
├── aerolinea_project/          # Configuración principal
│   ├── settings.py            # Configuraciones de Django
│   ├── urls.py               # URLs principales
│   └── wsgi.py               # Configuración WSGI
├── gestion_vuelos/            # Aplicación principal
│   ├── models.py             # Modelos de datos
│   ├── views.py              # Vistas y lógica de negocio
│   ├── forms.py              # Formularios
│   ├── admin.py              # Configuración del admin
│   └── urls.py               # URLs de la aplicación
├── templates/                 # Plantillas HTML
│   ├── base.html             # Plantilla base
│   ├── gestion_vuelos/       # Plantillas específicas
│   └── registration/         # Plantillas de autenticación
├── scripts/                   # Scripts de utilidad
│   └── crear_datos_ejemplo.py # Script para datos de prueba
├── requirements.txt           # Dependencias
└── README.md                 # Este archivo
\`\`\`

## Instalación y Configuración

### 1. Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 2. Instalación

\`\`\`bash
# Clonar o descargar el proyecto
cd sistema-aerolinea

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
\`\`\`

### 3. Configuración de la Base de Datos

\`\`\`bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear datos de ejemplo (opcional)
python scripts/crear_datos_ejemplo.py
\`\`\`

### 4. Ejecutar el Servidor

\`\`\`bash
# Iniciar servidor de desarrollo
python manage.py runserver

# El sistema estará disponible en: http://localhost:8000
\`\`\`

## Credenciales de Acceso

Después de ejecutar el script de datos de ejemplo:

- **Administrador**: `admin` / `admin123`
- **Empleado**: `empleado` / `empleado123`

Panel de administración: http://localhost:8000/admin/

## Modelos de Datos

### Entidades Principales

1. **Avión**: Información de la flota (modelo, capacidad, configuración)
2. **Vuelo**: Detalles de vuelos (origen, destino, fechas, precios)
3. **Pasajero**: Información personal de pasajeros
4. **Asiento**: Configuración de asientos por avión
5. **Reserva**: Reservas de vuelos con asientos específicos
6. **Boleto**: Boletos electrónicos generados
7. **PerfilUsuario**: Extensión de usuarios con roles

### Relaciones Implementadas

- Avión → Vuelo (1:N)
- Vuelo → Reserva (1:N)
- Pasajero → Reserva (1:N)
- Asiento → Reserva (1:1)
- Reserva → Boleto (1:1)

## Funcionalidades por Rol

### Administrador
- Acceso completo al panel de administración
- Gestión de vuelos, aviones, pasajeros
- Visualización de todos los reportes
- Gestión de usuarios y permisos

### Empleado
- Acceso al panel de administración
- Gestión de reservas y pasajeros
- Generación de reportes
- Consulta de información de vuelos

### Cliente
- Búsqueda y visualización de vuelos
- Creación de reservas
- Gestión de sus propias reservas
- Visualización de boletos

## Validaciones Implementadas

- **Documentos únicos**: No se permiten pasajeros con documentos duplicados
- **Asientos únicos**: Un asiento no puede reservarse más de una vez por vuelo
- **Reservas únicas**: Un pasajero no puede tener múltiples reservas en el mismo vuelo
- **Fechas válidas**: Validación de fechas de vuelos y nacimiento
- **Estados consistentes**: Los estados de asientos se actualizan automáticamente

## Características Técnicas

### Seguridad
- Protección CSRF habilitada
- Validación de formularios en backend y frontend
- Autenticación requerida para operaciones sensibles
- Roles y permisos diferenciados

### Performance
- Consultas optimizadas con select_related y prefetch_related
- Paginación en listados extensos
- Índices en campos de búsqueda frecuente

### Usabilidad
- Interfaz responsive con Bootstrap
- Mensajes informativos para el usuario
- Navegación intuitiva
- Búsquedas y filtros avanzados

## Posibles Mejoras Futuras

1. **Integración de Pagos**: Pasarela de pagos para reservas
2. **Notificaciones**: Sistema de emails automáticos
3. **API REST**: Endpoints para integración con apps móviles
4. **Reportes Avanzados**: Gráficos y estadísticas más detalladas
5. **Gestión de Equipaje**: Módulo para manejo de equipaje
6. **Check-in Online**: Sistema de check-in digital
7. **Multiidioma**: Soporte para múltiples idiomas

## Soporte y Contacto

Para consultas técnicas o reportar problemas, contactar al equipo de desarrollo.

---

**Desarrollado con Django para la Evaluación Final Integradora**
