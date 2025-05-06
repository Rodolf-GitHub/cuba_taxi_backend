# apps/auth/schemas.py
from ninja import Schema
from typing import Optional

class LoginRequest(Schema):
    """Datos necesarios para iniciar sesión"""
    username: str
    password: str

class TokenResponse(Schema):
    """Respuesta con el token de autenticación"""
    access_token: str
    token_type: str
    user_id: int
    username: str

class ErrorResponse(Schema):
    """Respuesta de error"""
    detail: str