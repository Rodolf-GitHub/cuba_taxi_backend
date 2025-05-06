from django.contrib.auth.models import User
from django.utils import timezone
from locations.data import get_municipio  # Importar función

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

def obtener_datos_usuario_perfil(user):
    """Obtiene los datos del usuario y su perfil para la respuesta"""
    # Verificar que no sea superusuario, excepto al obtener perfil propio
    if user.is_superuser:
        return None
        
    # Datos básicos en formato plano
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
        "disponibilidad": user.profile.disponibilidad,
        "ultima_disponibilidad": user.profile.ultima_disponibilidad,
        "municipio_id": user.profile.municipio_id
    }
    
    # Añadir información del municipio y provincia si existe
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