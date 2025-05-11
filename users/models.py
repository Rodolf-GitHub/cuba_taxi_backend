from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):
    """Perfil extendido para los usuarios de CubaTaxi"""
    
    # Opciones para tipo de vehículo
    TIPO_VEHICULO = [
        ('TAXI', 'Taxi'),
        ('MOTOCICLETA', 'Motocicleta'),
        ('CAMION', 'Camión'),
        ('FURGONETA', 'Furgoneta'),
        ('COCHE', 'Coche'),
        ('OTRO', 'Otro'),
    ]
    
    # Opciones para disponibilidad
    ESTADO_DISPONIBILIDAD = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADO', 'Ocupado'),
        ('NO_DISPONIBLE', 'No disponible'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    foto_vehiculo = models.ImageField(upload_to='vehicle_photos/', blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    municipio_id = models.CharField(max_length=4, blank=True, null=True,default="0803")
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPO_VEHICULO, default='TAXI')
    disponibilidad = models.CharField(max_length=20, choices=ESTADO_DISPONIBILIDAD, default='DISPONIBLE')
    ultima_disponibilidad = models.DateTimeField(default=timezone.now)
    capacidad_pasajeros = models.IntegerField(default=4)
    # Nuevos campos para la licencia
    fecha_ultima_licencia = models.DateTimeField(default=timezone.now)
    dias_licencia = models.IntegerField(default=30)  # Por defecto 30 días
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    def set_disponible(self):
        """Cambia el estado a disponible y actualiza la fecha"""
        self.disponibilidad = 'DISPONIBLE'
        self.ultima_disponibilidad = timezone.now()
        self.save()

    def licencia_vigente(self):
        """Verifica si la licencia está vigente"""
        if not self.fecha_ultima_licencia:
            return False
        fecha_vencimiento = self.fecha_ultima_licencia + timedelta(days=self.dias_licencia)
        return timezone.now() <= fecha_vencimiento

    def dias_restantes_licencia(self):
        """Calcula los días restantes de licencia"""
        if not self.fecha_ultima_licencia:
            return 0
        fecha_vencimiento = self.fecha_ultima_licencia + timedelta(days=self.dias_licencia)
        dias = (fecha_vencimiento - timezone.now()).days
        return max(0, dias)

# Señal para crear automáticamente un perfil cuando se crea un usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()