# apps/auth/endpoints.py
from ninja import Router
from django.http import HttpRequest
from .schemas import LoginRequest, TokenResponse, ErrorResponse
from .services import verificar_credenciales, crear_jwt_token
from .security import JWTAuth

# Crear router con tag de Autenticación
router = Router(tags=["Autenticación"])

@router.post("/login", response={200: TokenResponse, 401: ErrorResponse})
def login(request: HttpRequest, data: LoginRequest):
    """
    Iniciar sesión y obtener token de autenticación
    
    Proporciona un nombre de usuario y contraseña para obtener un token JWT
    """
    user = verificar_credenciales(data.username, data.password)
    
    if not user:
        return 401, {"detail": "Credenciales inválidas"}
    
    token = crear_jwt_token(user)
    
    return 200, {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@router.get("/me", response=TokenResponse, auth=JWTAuth())
def get_user_from_token(request):
    """
    Obtiene información del usuario actual basado en el token
    
    Requiere un token válido en el header de autorización
    """
    user = request.user
    
    return {
        "access_token": request.auth,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }