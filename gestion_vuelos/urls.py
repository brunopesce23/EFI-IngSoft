from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'gestion_vuelos'

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),
    
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    
    # Vuelos
    path('vuelos/', views.lista_vuelos, name='lista_vuelos'),
    path('vuelos/<int:vuelo_id>/', views.detalle_vuelo, name='detalle_vuelo'),
    path('buscar-vuelos/', views.buscar_vuelos, name='buscar_vuelos'),
    
    # Reservas
    path('reservar/<int:vuelo_id>/', views.crear_reserva, name='crear_reserva'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('reserva/<int:reserva_id>/', views.detalle_reserva, name='detalle_reserva'),
    path('cancelar-reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    
    # Pasajeros (solo admin)
    path('pasajeros/', views.lista_pasajeros, name='lista_pasajeros'),
    
    # Reportes (solo admin)
    path('reportes/', views.reportes, name='reportes'),
    path('reporte-vuelo/<int:vuelo_id>/', views.reporte_vuelo, name='reporte_vuelo'),
    
    # Boletos
    path('boleto/<int:boleto_id>/', views.ver_boleto, name='ver_boleto'),
    path('generar-boleto/<int:reserva_id>/', views.generar_boleto, name='generar_boleto'),

    # Paquetes (público)
    path('paquetes/', views.lista_paquetes, name='lista_paquetes'),
]
