# Sistema de Gestión de Aerolínea - Instrucciones de Instalación

## Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Instalar dependencias
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. Configurar la base de datos
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### 3. Crear superusuario (administrador)
\`\`\`bash
python manage.py createsuperuser
\`\`\`

### 4. Cargar datos de ejemplo
\`\`\`bash
python scripts/crear_datos_ejemplo.py
\`\`\`

### 5. Ejecutar el servidor
\`\`\`bash
python manage.py runserver
\`\`\`

## Acceso al Sistema

### URLs principales:
- **Página principal**: http://127.0.0.1:8000/
- **Panel de administración**: http://127.0.0.1:8000/admin/
- **Buscar vuelos**: http://127.0.0.1:8000/buscar-vuelos/
- **Lista de vuelos**: http://127.0.0.1:8000/vuelos/

### Usuarios de prueba (después de ejecutar el script):
- **Administrador**: admin / admin123
- **Empleado**: empleado / empleado123
- **Cliente**: cliente / cliente123

## Funcionalidades Implementadas

### ✅ Gestión de Vuelos
- Crear, editar, eliminar vuelos
- Búsqueda avanzada con filtros
- Vista detallada con mapa de asientos
- Control de estados (programado, en vuelo, completado, cancelado)

### ✅ Gestión de Pasajeros
- Registro de pasajeros con datos completos
- Validación de documentos
- Historial de vuelos por pasajero

### ✅ Sistema de Reservas
- Creación de reservas con selección de asientos
- Estados de reserva (pendiente, confirmada, pagada, cancelada)
- Códigos únicos de reserva
- Cancelación de reservas

### ✅ Boletos Electrónicos
- Generación automática de boletos
- Códigos de barra únicos
- Diseño profesional para impresión
- Estados de boleto (emitido, usado, cancelado)

### ✅ Panel de Administración
- Gestión completa de todas las entidades
- Filtros y búsquedas avanzadas
- Acciones en lote
- Interfaz intuitiva

### ✅ Autenticación y Autorización
- Sistema de login/registro
- Roles diferenciados (admin, empleado, cliente)
- Protección de vistas sensibles

### ✅ Reportes y Estadísticas
- Dashboard con métricas principales
- Reportes de ocupación
- Estadísticas de vuelos y reservas

### ✅ Interfaz Responsive
- Diseño adaptable a móviles y tablets
- Bootstrap 5 con iconos Font Awesome
- Experiencia de usuario optimizada

## Estructura del Proyecto

\`\`\`
aerolinea_project/
├── manage.py
├── requirements.txt
├── aerolinea_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── gestion_vuelos/
│   ├── models.py      # Modelos de datos
│   ├── views.py       # Lógica de vistas
│   ├── forms.py       # Formularios
│   ├── urls.py        # URLs de la aplicación
│   └── admin.py       # Configuración del admin
├── templates/
│   ├── base.html      # Template base
│   ├── gestion_vuelos/
│   └── registration/
└── scripts/
    └── crear_datos_ejemplo.py
\`\`\`

## Modelos de Base de Datos

### Avion
- modelo, capacidad, filas, columnas

### Vuelo
- codigo_vuelo, origen, destino, fechas, precio, estado
- Relación con Avion

### Pasajero
- nombre, email, telefono, documento, fecha_nacimiento
- Relación con User (opcional)

### Asiento
- numero, tipo (economica, ejecutiva, primera)
- Relación con Avion

### Reserva
- codigo_reserva, fecha_reserva, estado, precio
- Relaciones con Vuelo, Pasajero, Asiento

### Boleto
- codigo_barra, fecha_emision, estado
- Relación con Reserva

## Características Técnicas

- **Framework**: Django 4.2
- **Base de datos**: SQLite (local)
- **Frontend**: Bootstrap 5 + Font Awesome
- **Autenticación**: Sistema integrado de Django
- **Validaciones**: Backend y frontend
- **Paginación**: Implementada en todas las listas
- **Mensajes**: Sistema de notificaciones
- **Responsive**: Diseño móvil-first

## Próximas Mejoras Sugeridas

1. **Pagos en línea**: Integración con pasarelas de pago
2. **Notificaciones**: Email/SMS para confirmaciones
3. **API REST**: Para aplicaciones móviles
4. **Reportes avanzados**: Gráficos y exportación
5. **Check-in online**: Funcionalidad de check-in
6. **Gestión de equipaje**: Control de maletas
7. **Programa de fidelidad**: Sistema de puntos
8. **Multi-idioma**: Soporte para varios idiomas

## Soporte

Para dudas o problemas, revisa:
1. Los logs del servidor Django
2. La documentación de Django
3. Los comentarios en el código fuente

¡El sistema está listo para usar y presentar en tu evaluación final!
