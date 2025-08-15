from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10, verbose_name='Número de asiento')),
                ('fila', models.PositiveIntegerField(verbose_name='Fila')),
                ('columna', models.CharField(max_length=1, verbose_name='Columna')),
                ('tipo', models.CharField(choices=[('economica', 'Clase Económica'), ('ejecutiva', 'Clase Ejecutiva'), ('primera', 'Primera Clase')], default='economica', max_length=20)),
                ('estado', models.CharField(choices=[('disponible', 'Disponible'), ('reservado', 'Reservado'), ('ocupado', 'Ocupado'), ('mantenimiento', 'En Mantenimiento')], default='disponible', max_length=20)),
            ],
            options={
                'verbose_name': 'Asiento',
                'verbose_name_plural': 'Asientos',
                'ordering': ['fila', 'columna'],
            },
        ),
        migrations.CreateModel(
            name='Avion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=100, verbose_name='Modelo')),
                ('capacidad', models.PositiveIntegerField(verbose_name='Capacidad total')),
                ('filas', models.PositiveIntegerField(verbose_name='Número de filas')),
                ('columnas', models.PositiveIntegerField(verbose_name='Asientos por fila')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Avión',
                'verbose_name_plural': 'Aviones',
            },
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('destino', models.CharField(max_length=120)),
                ('descripcion', models.TextField()),
                ('precio_desde', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duracion_noches', models.PositiveIntegerField(default=7)),
                ('incluye', models.TextField(help_text='Lista o texto con servicios incluidos')),
                ('imagen_url', models.URLField(blank=True, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Paquete',
                'verbose_name_plural': 'Paquetes',
            },
        ),
        migrations.CreateModel(
            name='Pasajero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre completo')),
                ('documento', models.CharField(max_length=20, unique=True, verbose_name='Número de documento')),
                ('tipo_documento', models.CharField(choices=[('dni', 'DNI'), ('pasaporte', 'Pasaporte'), ('cedula', 'Cédula')], default='dni', max_length=10)),
                ('email', models.EmailField(max_length=254, verbose_name='Correo electrónico')),
                ('telefono', models.CharField(max_length=20, verbose_name='Teléfono')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Pasajero',
                'verbose_name_plural': 'Pasajeros',
            },
        ),
        migrations.CreateModel(
            name='Vuelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origen', models.CharField(max_length=100, verbose_name='Ciudad de origen')),
                ('destino', models.CharField(max_length=100, verbose_name='Ciudad de destino')),
                ('fecha_salida', models.DateTimeField(verbose_name='Fecha y hora de salida')),
                ('fecha_llegada', models.DateTimeField(verbose_name='Fecha y hora de llegada')),
                ('duracion', models.DurationField(blank=True, null=True, verbose_name='Duración del vuelo')),
                ('estado', models.CharField(choices=[('programado', 'Programado'), ('abordando', 'Abordando'), ('en_vuelo', 'En Vuelo'), ('aterrizado', 'Aterrizado'), ('cancelado', 'Cancelado'), ('retrasado', 'Retrasado')], default='programado', max_length=20)),
                ('precio_base', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio base')),
                ('codigo_vuelo', models.CharField(max_length=10, unique=True, verbose_name='Código de vuelo')),
                ('avion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vuelos', to='gestion_vuelos.avion')),
            ],
            options={
                'verbose_name': 'Vuelo',
                'verbose_name_plural': 'Vuelos',
                'ordering': ['fecha_salida'],
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada'), ('pagada', 'Pagada'), ('cancelada', 'Cancelada'), ('completada', 'Completada')], default='pendiente', max_length=20)),
                ('fecha_reserva', models.DateTimeField(auto_now_add=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio final')),
                ('codigo_reserva', models.CharField(max_length=10, unique=True, verbose_name='Código de reserva')),
                ('asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='gestion_vuelos.asiento')),
                ('pasajero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='gestion_vuelos.pasajero')),
                ('vuelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='gestion_vuelos.vuelo')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'ordering': ['-fecha_reserva'],
                'unique_together': {('vuelo', 'asiento')},
            },
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('admin', 'Administrador'), ('cliente', 'Cliente')], default='cliente', max_length=20)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil de Usuario',
                'verbose_name_plural': 'Perfiles de Usuario',
            },
        ),
        migrations.CreateModel(
            name='Boleto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_barra', models.CharField(max_length=50, unique=True, verbose_name='Código de barras')),
                ('fecha_emision', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('emitido', 'Emitido'), ('usado', 'Usado'), ('cancelado', 'Cancelado')], default='emitido', max_length=20)),
                ('reserva', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='boleto', to='gestion_vuelos.reserva')),
            ],
            options={
                'verbose_name': 'Boleto',
                'verbose_name_plural': 'Boletos',
            },
        ),
        migrations.AddField(
            model_name='asiento',
            name='avion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asientos', to='gestion_vuelos.avion'),
        ),
        migrations.AlterUniqueTogether(
            name='asiento',
            unique_together={('avion', 'numero')},
        ),
    ]
