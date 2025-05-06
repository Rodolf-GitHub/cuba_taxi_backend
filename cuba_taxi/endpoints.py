from ninja import NinjaAPI
from users.endpoints import router as users_router
from auth.endpoints import router as auth_router
from locations.endpoints import router as locations_router

# Asegúrate de que la configuración esté así
api = NinjaAPI(
    title="CubaTaxi API",
    version="1.0.0",
    description="API para la aplicación CubaTaxi",
    docs_url="/documentacion",  # Especifica explícitamente la URL de la documentación
    urls_namespace="api"
)

api.add_router("/users", users_router)
api.add_router("/auth", auth_router)
api.add_router("/locations", locations_router)