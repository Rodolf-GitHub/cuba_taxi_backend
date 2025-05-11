# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Profile
from django.utils import timezone

# Define una clase Admin para el modelo Profile
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('usuario_completo', 'telefono', 'tipo_vehiculo', 'disponibilidad', 'ultima_disponibilidad', 'foto_perfil', 'foto_vehiculo_preview')
    list_filter = ('tipo_vehiculo', 'disponibilidad')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'telefono')
    readonly_fields = ('ultima_disponibilidad',)
    date_hierarchy = 'ultima_disponibilidad'
    
    def usuario_completo(self, obj):
        """Muestra el nombre completo del usuario"""
        return f"{obj.user.first_name} {obj.user.last_name} ({obj.user.username})"
    usuario_completo.short_description = "Usuario"
    
    def foto_perfil(self, obj):
        """Muestra una vista previa de la foto de perfil"""
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_picture.url)
        return "Sin foto"
    foto_perfil.short_description = "Foto"
    
    def foto_vehiculo_preview(self, obj):
        """Muestra una vista previa de la foto del vehículo"""
        if obj.foto_vehiculo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.foto_vehiculo.url)
        return "Sin foto"
    foto_vehiculo_preview.short_description = "Vehículo"
    
    # Acciones personalizadas
    actions = ['marcar_disponible', 'marcar_no_disponible']
    
    def marcar_disponible(self, request, queryset):
        """Acción para marcar usuarios como disponibles"""
        for profile in queryset:
            profile.disponibilidad = 'DISPONIBLE'
            profile.ultima_disponibilidad = timezone.now()
            profile.save()
        self.message_user(request, f"{queryset.count()} perfiles marcados como disponibles.")
    marcar_disponible.short_description = "Marcar como disponibles"
    
    def marcar_no_disponible(self, request, queryset):
        """Acción para marcar usuarios como no disponibles"""
        queryset.update(disponibilidad='NO_DISPONIBLE')
        self.message_user(request, f"{queryset.count()} perfiles marcados como no disponibles.")
    marcar_no_disponible.short_description = "Marcar como no disponibles"

# Registrar el admin para Profile
admin.site.register(Profile, ProfileAdmin)

# Definir un admin personalizado para User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fieldsets = (
        (None, {
            'fields': ('profile_picture', 'foto_vehiculo', 'telefono', 'municipio_id')
        }),
        ('Información del Vehículo', {
            'fields': ('tipo_vehiculo', 'capacidad_pasajeros')
        }),
        ('Estado', {
            'fields': ('disponibilidad', 'ultima_disponibilidad')
        }),
        ('Licencia', {
            'fields': ('fecha_ultima_licencia', 'dias_licencia'),
            'description': 'Configure los días de licencia y la fecha de última actualización'
        })
    )

# Redefine el UserAdmin para incluir el perfil
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_dias_restantes')
    
    def get_dias_restantes(self, obj):
        return obj.profile.dias_restantes_licencia()
    get_dias_restantes.short_description = 'Días de Licencia Restantes'

# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)