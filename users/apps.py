from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import sys
        # Evitar iniciar el scheduler en comandos de gestión o migraciones
        if 'runserver' in sys.argv or 'uvicorn' in sys.argv:
            try:
                from .scheduler import iniciar_scheduler
                iniciar_scheduler()
                logger.info("Scheduler iniciado desde UsersConfig.ready()")
            except Exception as e:
                logger.error(f"Error al iniciar scheduler: {e}")
