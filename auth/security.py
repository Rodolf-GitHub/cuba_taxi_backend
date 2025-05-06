# apps/auth/security.py
import jwt
from django.conf import settings
from ninja.security import HttpBearer
from django.contrib.auth.models import User
from datetime import datetime

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            # Decodificar el token
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256']
            )
            
            # Verificar expiración
            exp = datetime.fromtimestamp(payload.get('exp'))
            if datetime.utcnow() > exp:
                return None
                
            # Obtener usuario
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
            
            # Adjuntar usuario a la request
            request.user = user
            
            return token
        except (jwt.PyJWTError, User.DoesNotExist):
            return None