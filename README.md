# Proyecto Sistema de Aerolínea (Django)

## 📌 Descripción general
Este proyecto es un sistema web desarrollado como trabajo práctico integrador para la materia Ingeniería de Software.  
Permite la **gestión de vuelos y paquetes turísticos**, con carga de datos, visualización y administración desde el panel de Django.

## 📁 Estructura del proyecto
/aerolinea_project
├── settings.py # Configuración general del proyecto
├── urls.py # Rutas principales
└── wsgi.py / asgi.py # Configuración de despliegue

/gestion_vuelos
├── migrations/ # Migraciones de base de datos
├── templates/ # Plantillas HTML específicas del módulo
├── models.py # Modelos de Vuelos, Paquetes, Asientos, etc.
├── views.py # Lógica de vistas
├── urls.py # Rutas del módulo
└── admin.py # Configuración de Django admin

/templates
├── base.html # Plantilla base
├── gestion_vuelos/ # Vistas como lista_vuelos, detalle_vuelo, paquetes
└── registration/ # Plantillas para login y registro

/static
└── (archivos estáticos: CSS, imágenes, etc.)

manage.py # Script principal de Django
requirements.txt # Dependencias del proyecto

bash
Copiar
Editar

## 🧩 Funcionalidades
✅ Carga y visualización de vuelos nacionales e internacionales  
✅ Gestión de paquetes turísticos  
✅ Sistema de plantillas con herencia (`base.html`)  
✅ Panel de administración de Django para CRUD completo  
✅ Separación de modelos, vistas y rutas  

## 🚀 Instrucciones para correr el proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/brunopesce23/EFI-IngSoft
cd EFI-IngSoft
2. Crear y activar entorno virtual
bash
Copiar
Editar
python -m venv .venv
source .venv/bin/activate
3. Instalar dependencias
bash
Copiar
Editar
pip install -r requirements.txt
4. Aplicar migraciones
bash
Copiar
Editar
python manage.py migrate
5. Crear superusuario (opcional)
bash
Copiar
Editar
python manage.py createsuperuser
6. Levantar el servidor
bash
Copiar
Editar
python manage.py runserver
Servidor disponible en: http://127.0.0.1:8000/

🛠️ Tecnologías utilizadas
Backend:

Python 3.10+

Django 4.x

SQLite (desarrollo)

Frontend (templates):

HTML5

CSS3

Django Template Language (DTL)

📝 Consigna cumplida
CRUD funcional para vuelos y paquetes turísticos

Gestión desde panel de administración de Django

Sistema de plantillas con herencia

Base de datos SQLite para desarrollo