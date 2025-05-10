from ninja import Schema
from typing import Optional
from pydantic import EmailStr
from datetime import datetime
from enum import Enum

# Enumeraciones para validación
class TipoVehiculo(str, Enum):
    TAXI = "TAXI"
    MOTOCICLETA = "MOTOCICLETA" 
    CAMION = "CAMION"
    FURGONETA = "FURGONETA"
    COCHE = "COCHE"
    OTRO = "OTRO"

class EstadoDisponibilidad(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    OCUPADO = "OCUPADO"
    NO_DISPONIBLE = "NO_DISPONIBLE"

# Esquemas de petición (entrada)
class CrearUsuarioSchema(Schema):
    """Esquema para crear un nuevo usuario"""
    username: str
    email: EmailStr
    password: str
    telefono: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tipo_vehiculo: Optional[TipoVehiculo] = TipoVehiculo.TAXI
    capacidad_pasajeros: Optional[int] = 4
    disponibilidad: Optional[EstadoDisponibilidad] = EstadoDisponibilidad.DISPONIBLE
    municipio_id: Optional[str] = None

class ActualizarPerfilSchema(Schema):
    """Esquema para actualizar perfil"""
    tipo_vehiculo: Optional[TipoVehiculo] = None
    capacidad_pasajeros: Optional[int] = None
    disponibilidad: Optional[EstadoDisponibilidad] = None
    telefono: Optional[str] = None
    municipio_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

class CambiarEstadoSchema(Schema):
    """Esquema para cambiar estado de disponibilidad"""
    estado: EstadoDisponibilidad

class CambiarPasswordSchema(Schema):
    """Esquema para cambiar la contraseña del usuario"""
    password_actual: str
    password_nueva: str
    confirmar_password: str

class MensajeRespuestaSchema(Schema):
    """Esquema para mensajes de respuesta simples"""
    mensaje: str

# Esquemas de respuesta (salida)
class PerfilSchema(Schema):
    """Esquema del perfil para respuestas"""
    profile_picture: Optional[str] = None
    foto_vehiculo: Optional[str] = None
    tipo_vehiculo: TipoVehiculo
    capacidad_pasajeros: Optional[int] = None
    disponibilidad: EstadoDisponibilidad
    ultima_disponibilidad: datetime
    tiempo_disponibilidad_restante: Optional[int] = None  # en minutos
    telefono: Optional[str] = None
    municipio_id: Optional[str] = None
    municipio_nombre: Optional[str] = None
    provincia_id: Optional[str] = None
    provincia_nombre: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

class UsuarioSchema(Schema):
    """Esquema de usuario para respuestas"""
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    telefono: Optional[str] = None
    profile_picture: Optional[str] = None
    foto_vehiculo: Optional[str] = None
    tipo_vehiculo: TipoVehiculo
    capacidad_pasajeros: Optional[int] = None
    disponibilidad: EstadoDisponibilidad
    ultima_disponibilidad: datetime
    municipio_id: Optional[str] = None
    municipio_nombre: Optional[str] = None
    provincia_id: Optional[str] = None
    provincia_nombre: Optional[str] = None

class ListaUsuariosSchema(Schema):
    """Esquema resumido para listar usuarios"""
    id: int
    username: str
    profile_picture: Optional[str] = None
    tipo_vehiculo: TipoVehiculo
    capacidad_pasajeros: Optional[int] = None
    disponibilidad: EstadoDisponibilidad
    telefono: Optional[str] = None
    municipio_id: Optional[str] = None
    municipio_nombre: Optional[str] = None
    provincia_id: Optional[str] = None
    provincia_nombre: Optional[str] = None

class RespuestaEstadoSchema(Schema):
    """Esquema para respuesta de cambio de estado"""
    disponibilidad: EstadoDisponibilidad
    ultima_disponibilidad: datetime