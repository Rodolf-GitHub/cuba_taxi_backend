from ninja import Router, File
from ninja.files import UploadedFile
from auth.security import JWTAuth
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from typing import List
from locations.data import get_municipio


from .schemas import (
    CrearUsuarioSchema, 
    ActualizarPerfilSchema, 
    CambiarEstadoSchema,
    UsuarioSchema,
    ListaUsuariosSchema,
    PerfilSchema,
    RespuestaEstadoSchema,
    CambiarPasswordSchema,
    MensajeRespuestaSchema
)
from .services import (
    crear_usuario,
    actualizar_perfil,
    cambiar_estado,
    set_disponible,
    obtener_datos_usuario_perfil,
    cambiar_password
)

router = Router(tags=["Usuarios"])

@router.post("/register", response=UsuarioSchema)
def registrar_usuario(request, data: CrearUsuarioSchema):
    """Registrar un nuevo usuario"""
    user = crear_usuario(
        username=data.username,
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name,
        tipo_vehiculo=data.tipo_vehiculo,
        capacidad_pasajeros=data.capacidad_pasajeros,
        disponibilidad=data.disponibilidad,
        telefono=data.telefono,
        municipio_id=data.municipio_id
    )
    
    return obtener_datos_usuario_perfil(user)

@router.get("/me", response=PerfilSchema, auth=JWTAuth())
def obtener_mi_perfil(request):
    """Obtener el perfil del usuario autenticado"""
    return obtener_datos_usuario_perfil(request.user)

@router.put("/me", response=PerfilSchema, auth=JWTAuth())
def actualizar_mi_perfil(request, data: ActualizarPerfilSchema, profile_picture: UploadedFile = File(None), foto_vehiculo: UploadedFile = File(None)):
    """Actualizar el perfil del usuario autenticado y sus datos personales"""
    profile, user = actualizar_perfil(
        user=request.user,
        tipo_vehiculo=data.tipo_vehiculo,
        capacidad_pasajeros=data.capacidad_pasajeros,
        disponibilidad=data.disponibilidad,
        profile_picture=profile_picture,
        foto_vehiculo=foto_vehiculo,
        telefono=data.telefono,
        municipio_id=data.municipio_id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email
    )
    
    # Obtener información del municipio
    municipio_data = {
        "municipio_id": profile.municipio_id,
        "municipio_nombre": None,
        "provincia_id": None,
        "provincia_nombre": None
    }
    
    if profile.municipio_id:
        municipio_info = get_municipio(profile.municipio_id)
        if municipio_info:
            municipio_data["municipio_nombre"] = municipio_info["nombre"]
            municipio_data["provincia_id"] = municipio_info["provincia_id"]
            municipio_data["provincia_nombre"] = municipio_info["provincia_nombre"]
    
    # Construir la respuesta con todos los datos
    return {
        "profile_picture": profile.profile_picture.url if profile.profile_picture else None,
        "foto_vehiculo": profile.foto_vehiculo.url if profile.foto_vehiculo else None,
        "tipo_vehiculo": profile.tipo_vehiculo,
        "capacidad_pasajeros": profile.capacidad_pasajeros,
        "disponibilidad": profile.disponibilidad,
        "ultima_disponibilidad": profile.ultima_disponibilidad,
        "telefono": profile.telefono,
        **municipio_data,  # Incluir datos del municipio
        # También incluir los datos actualizados del usuario
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }

@router.get("", response=List[ListaUsuariosSchema])
def listar_usuarios(request):
    """Listar todos los usuarios excepto superusuarios y con licencia vigente"""
    # Excluimos a los superusuarios
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    
    result = []
    for user in users:
        # Solo incluir usuarios con licencia vigente
        if user.profile.licencia_vigente():
            user_dict = {
                "id": user.id,
                "username": user.username,
                "profile_picture": user.profile.profile_picture.url if user.profile.profile_picture else None,
                "tipo_vehiculo": user.profile.tipo_vehiculo,
                "capacidad_pasajeros": user.profile.capacidad_pasajeros,
                "disponibilidad": user.profile.disponibilidad,
                "telefono": user.profile.telefono,
                "municipio_id": user.profile.municipio_id,
                "fecha_ultima_licencia": user.profile.fecha_ultima_licencia,
                "dias_licencia": user.profile.dias_licencia,
                "dias_restantes_licencia": user.profile.dias_restantes_licencia()
            }
            
            # Añadir información del municipio y provincia si existe
            if user.profile.municipio_id:
                municipio_info = get_municipio(user.profile.municipio_id)
                if municipio_info:
                    user_dict["municipio_nombre"] = municipio_info["nombre"]
                    user_dict["provincia_id"] = municipio_info["provincia_id"]
                    user_dict["provincia_nombre"] = municipio_info["provincia_nombre"]
            
            result.append(user_dict)
    
    return result

@router.get("/{int:user_id}", response=UsuarioSchema)
def obtener_usuario(request, user_id: int):
    """Obtener datos de un usuario específico (no superusuarios)"""
    user = get_object_or_404(User, id=user_id, is_superuser=False)
    return obtener_datos_usuario_perfil(user)

@router.post("/set-disponible", response=RespuestaEstadoSchema, auth=JWTAuth())
def establecer_disponible(request):
    """Cambiar estado a disponible"""
    profile = set_disponible(request.user)
    
    return {
        "disponibilidad": profile.disponibilidad,
        "ultima_disponibilidad": profile.ultima_disponibilidad
    }

@router.post("/cambiar-estado", response=RespuestaEstadoSchema, auth=JWTAuth())
def cambiar_estado_usuario(request, data: CambiarEstadoSchema):
    """Cambiar estado de disponibilidad"""
    profile = cambiar_estado(request.user, data.estado)
    
    return {
        "disponibilidad": profile.disponibilidad,
        "ultima_disponibilidad": profile.ultima_disponibilidad
    }

@router.post(
    "/cambiar-password", 
    response={200: MensajeRespuestaSchema, 400: MensajeRespuestaSchema}, 
    auth=JWTAuth()
)
def cambiar_password_endpoint(request, data: CambiarPasswordSchema):
    """Cambiar la contraseña del usuario autenticado"""
    # Verificar que las contraseñas nuevas coincidan
    if data.password_nueva != data.confirmar_password:
        return 400, {"mensaje": "Las contraseñas nuevas no coinciden"}
    
    # Verificar reglas de seguridad básicas
    if len(data.password_nueva) < 8:
        return 400, {"mensaje": "La contraseña debe tener al menos 8 caracteres"}
    
    # Cambiar la contraseña usando el servicio
    success, message = cambiar_password(
        user=request.user,
        password_actual=data.password_actual,
        password_nueva=data.password_nueva
    )
    
    if not success:
        return 400, {"mensaje": message}
    
    return 200, {"mensaje": message}