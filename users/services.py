from django.contrib.auth.models import User
from django.utils import timezone
from locations.data import get_municipio  # Importar función
from datetime import datetime, timedelta

def crear_usuario(username, email, password, first_name="", last_name="", tipo_vehiculo=None, capacidad_pasajeros=None, disponibilidad=None, telefono=None, municipio_id=None):
    """Crea un nuevo usuario con su perfil"""
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name or "",
        last_name=last_name or ""
    )
    
    # Actualizar perfil con todos los datos
    profile = user.profile
    if tipo_vehiculo:
        profile.tipo_vehiculo = tipo_vehiculo
    if capacidad_pasajeros:
        profile.capacidad_pasajeros = capacidad_pasajeros
    if disponibilidad:
        profile.disponibilidad = disponibilidad
    if telefono:
        profile.telefono = telefono  # Guardar teléfono
    if municipio_id:
        profile.municipio_id = municipio_id  # Guardar municipio
    profile.save()
    
    return user

def actualizar_perfil(user, tipo_vehiculo=None, disponibilidad=None, 
                      profile_picture=None, foto_vehiculo=None, telefono=None, municipio_id=None,
                      first_name=None, last_name=None, email=None, capacidad_pasajeros=None):  # Nuevos parámetros
    """Actualiza el perfil de un usuario y sus datos personales"""
    # Actualizar datos del usuario
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if email is not None:
        user.email = email
    user.save()  # Guardar los cambios en el usuario
    
    # Actualizar datos del perfil
    profile = user.profile
    if tipo_vehiculo:
        profile.tipo_vehiculo = tipo_vehiculo
    if disponibilidad:
        profile.disponibilidad = disponibilidad
    if capacidad_pasajeros:
        profile.capacidad_pasajeros = capacidad_pasajeros
    if profile_picture:
        profile.profile_picture = profile_picture
    if foto_vehiculo:
        profile.foto_vehiculo = foto_vehiculo
    if telefono:
        profile.telefono = telefono
    if municipio_id:
        profile.municipio_id = municipio_id
    
    profile.save()
    return profile, user  # Devolver tanto el perfil como el usuario actualizado

def cambiar_estado(user, estado):
    """Cambia el estado de disponibilidad"""
    profile = user.profile
    profile.disponibilidad = estado
    
    if estado == "DISPONIBLE":
        profile.ultima_disponibilidad = timezone.now()
    
    profile.save()
    return profile

def set_disponible(user):
    """Cambia el estado a disponible"""
    profile = user.profile
    profile.disponibilidad = "DISPONIBLE"
    profile.ultima_disponibilidad = timezone.now()
    profile.save()
    return profile

def calcular_tiempo_restante(ultima_disponibilidad):
    """Calcula los minutos restantes antes de que se desactive la disponibilidad"""
    try:
        # Obtener tiempo actual
        tiempo_actual = timezone.now()
        
        # Asegurar que ultima_disponibilidad sea datetime con timezone
        if isinstance(ultima_disponibilidad, str):
            from django.utils.dateparse import parse_datetime
            ultima_disponibilidad = parse_datetime(ultima_disponibilidad)
        
        if ultima_disponibilidad.tzinfo is None:
            ultima_disponibilidad = timezone.make_aware(ultima_disponibilidad)
            
        # Calcular tiempo límite (12 horas después de ultima_disponibilidad)
        tiempo_limite = ultima_disponibilidad + timedelta(hours=12)
        
        # Debug prints
        print("DEBUG - Tiempos:")
        print(f"Actual: {tiempo_actual}")
        print(f"Última disponibilidad: {ultima_disponibilidad}")
        print(f"Límite: {tiempo_limite}")
        
        # Si el tiempo actual es menor que la última disponibilidad (fecha futura)
        if tiempo_actual < ultima_disponibilidad:
            diferencia = ultima_disponibilidad + timedelta(hours=12) - tiempo_actual
            minutos_restantes = int(diferencia.total_seconds() / 60)
            print(f"Tiempo restante para fecha futura: {minutos_restantes} minutos")
            return minutos_restantes
            
        # Si aún no ha pasado el tiempo límite
        if tiempo_actual < tiempo_limite:
            diferencia = tiempo_limite - tiempo_actual
            minutos_restantes = int(diferencia.total_seconds() / 60)
            print(f"Tiempo restante: {minutos_restantes} minutos")
            return minutos_restantes
            
        print("Tiempo expirado")
        return 0
        
    except Exception as e:
        print(f"Error en calcular_tiempo_restante: {str(e)}")
        return 0

def obtener_datos_usuario_perfil(user):
    """Obtiene los datos del usuario y su perfil para la respuesta"""
    if user.is_superuser:
        return None
    
    # Calcular tiempo restante de disponibilidad
    tiempo_restante = calcular_tiempo_restante(user.profile.ultima_disponibilidad)
    
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "telefono": user.profile.telefono,
        "profile_picture": user.profile.profile_picture.url if user.profile.profile_picture else None,
        "foto_vehiculo": user.profile.foto_vehiculo.url if user.profile.foto_vehiculo else None,
        "tipo_vehiculo": user.profile.tipo_vehiculo,
        "capacidad_pasajeros": user.profile.capacidad_pasajeros,
        "disponibilidad": user.profile.disponibilidad,  # Ya no modificamos el estado
        "ultima_disponibilidad": user.profile.ultima_disponibilidad,
        "tiempo_disponibilidad_restante": tiempo_restante,
        "fecha_ultima_licencia": user.profile.fecha_ultima_licencia,
        "dias_licencia": user.profile.dias_licencia,
        "dias_restantes_licencia": user.profile.dias_restantes_licencia(),
        "municipio_id": user.profile.municipio_id
    }
    
    # Añadir información del municipio y provincia
    if user.profile.municipio_id:
        municipio_info = get_municipio(user.profile.municipio_id)
        if municipio_info:
            data["municipio_nombre"] = municipio_info["nombre"]
            data["provincia_id"] = municipio_info["provincia_id"]
            data["provincia_nombre"] = municipio_info["provincia_nombre"]
    
    return data

def cambiar_password(user, password_actual, password_nueva):
    """
    Cambia la contraseña del usuario si la contraseña actual es correcta
    
    Retorna (success, message) donde success es un booleano y message un mensaje
    """
    # Verificar que la contraseña actual sea correcta
    if not user.check_password(password_actual):
        return False, "La contraseña actual es incorrecta"
    
    # Cambiar la contraseña
    user.set_password(password_nueva)
    user.save()
    
    return True, "Contraseña actualizada correctamente"