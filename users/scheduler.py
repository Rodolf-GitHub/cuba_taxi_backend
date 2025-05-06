# apps/users/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from datetime import timedelta
from .models import Profile

def actualizar_disponibilidad():
    """
    Cambia el estado a NO_DISPONIBLE para usuarios cuya última actualización 
    fue hace más de 12 horas (y que no estén ya en estado NO_DISPONIBLE)
    """
    # Calcular el límite de tiempo (12 horas atrás)
    limite_tiempo = timezone.now() - timedelta(hours=12)
    
    # Encontrar perfiles que NO están en estado NO_DISPONIBLE
    # y cuya última actualización fue hace más de 12 horas
    perfiles_inactivos = Profile.objects.exclude(
        disponibilidad='NO_DISPONIBLE'
    ).filter(
        ultima_disponibilidad__lt=limite_tiempo
    )
    
    # Cambiar el estado
    cantidad = perfiles_inactivos.count()
    if cantidad > 0:
        perfiles_inactivos.update(disponibilidad='NO_DISPONIBLE')
        print(f"Se cambiaron {cantidad} perfiles a NO_DISPONIBLE")
    else:
        print("No hay perfiles que necesiten actualización")

def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    # Programar la tarea para que se ejecute cada hora
    scheduler.add_job(
        actualizar_disponibilidad,
        'interval',
        hours=1,  # Ejecutar cada hora (puedes ajustar según necesites)
        name='actualizar_disponibilidad',
        jobstore='default',
        id='actualizar_disponibilidad',
        replace_existing=True,
    )
    
    scheduler.start()
    print("Scheduler iniciado. La tarea de actualización de disponibilidad se ejecutará cada hora.")