# apps/auth/services.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja.security import django_auth
import jwt
from django.conf import settings
from datetime import datetime, timedelta
import uuid

# Para simplificar, usaremos JWT. En un entorno de producción,
# considera usar REST framework's TokenAuthentication o django-rest-knox

def crear_jwt_token(user):
    """Crea un token JWT para un usuario"""
    # Fecha de emisión y expiración
    now = datetime.utcnow()
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': now + timedelta(hours=24),  # Token válido por 24 horas
        'iat': now,
        'jti': str(uuid.uuid4())  # ID único para el token
    }
    
    # Crear token
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm='HS256'
    )
    
    return token

def verificar_credenciales(username, password):
    """Verifica las credenciales del usuario"""
    user = authenticate(username=username, password=password)
    return user