from django import forms
from django.core.exceptions import ValidationError
from .models import Pasajero, Reserva, Asiento


class PasajeroForm(forms.ModelForm):
    """Formulario para registro de pasajeros"""
    
    class Meta:
        model = Pasajero
        fields = ['nombre', 'documento', 'tipo_documento', 'email', 'telefono', 'fecha_nacimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de documento'
            }),
            'tipo_documento': forms.Select(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+54 11 1234-5678'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def clean_documento(self):
        documento = self.cleaned_data['documento']
        if Pasajero.objects.filter(documento=documento).exists():
            raise ValidationError('Ya existe un pasajero con este número de documento.')
        return documento


class ReservaForm(forms.ModelForm):
    """Formulario para crear reservas"""
    
    class Meta:
        model = Reserva
        fields = ['pasajero', 'asiento']
        widgets = {
            'pasajero': forms.Select(attrs={
                'class': 'form-control'
            }),
            'asiento': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.vuelo = kwargs.pop('vuelo', None)
        super().__init__(*args, **kwargs)
        
        if self.vuelo:
            # Filtrar asientos disponibles para este vuelo
            asientos_reservados = Reserva.objects.filter(
                vuelo=self.vuelo,
                estado__in=['confirmada', 'pagada']
            ).values_list('asiento_id', flat=True)
            
            self.fields['asiento'].queryset = Asiento.objects.filter(
                avion=self.vuelo.avion,
                estado='disponible'
            ).exclude(id__in=asientos_reservados)
    
    def clean(self):
        cleaned_data = super().clean()
        pasajero = cleaned_data.get('pasajero')
        asiento = cleaned_data.get('asiento')
        
        if pasajero and self.vuelo:
            # Verificar que el pasajero no tenga ya una reserva en este vuelo
            if Reserva.objects.filter(
                vuelo=self.vuelo,
                pasajero=pasajero,
                estado__in=['confirmada', 'pagada']
            ).exists():
                raise ValidationError('Este pasajero ya tiene una reserva en este vuelo.')
        
        if asiento and self.vuelo:
            # Verificar que el asiento no esté ya reservado
            if Reserva.objects.filter(
                vuelo=self.vuelo,
                asiento=asiento,
                estado__in=['confirmada', 'pagada']
            ).exists():
                raise ValidationError('Este asiento ya está reservado.')
        
        return cleaned_data


class BusquedaVueloForm(forms.Form):
    """Formulario para búsqueda de vuelos"""
    origen = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ciudad de origen'
        })
    )
    destino = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ciudad de destino'
        })
    )
    fecha_salida = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
