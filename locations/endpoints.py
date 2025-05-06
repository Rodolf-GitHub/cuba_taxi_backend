# apps/locations/endpoints.py
from ninja import Router
from typing import Dict, List
from .schemas import ProvinciaSchema, MunicipioSchema, ProvinciaConMunicipiosSchema
from .data import (
    get_all_provincias, 
    get_provincia, 
    get_all_municipios, 
    get_municipios_by_provincia,
    get_municipio
)

router = Router(tags=["Ubicaciones"])

@router.get("/provincias", response=Dict[str, str])
def listar_provincias(request):
    """Devuelve todas las provincias de Cuba"""
    return get_all_provincias()

@router.get("/provincias/{id_provincia}", response=ProvinciaConMunicipiosSchema)
def obtener_provincia(request, id_provincia: str):
    """Devuelve los datos de una provincia específica con sus municipios"""
    provincia = get_provincia(id_provincia)
    if not provincia:
        return {"detail": "Provincia no encontrada"}, 404
    
    return {
        "id": id_provincia,
        "nombre": provincia["nombre"],
        "municipios": provincia["municipios"]
    }



@router.get("/municipios/provincia/{id_provincia}", response=Dict[str, str])
def obtener_municipios_provincia(request, id_provincia: str):
    """Devuelve los municipios de una provincia específica"""
    municipios = get_municipios_by_provincia(id_provincia)
    if not municipios:
        return {"detail": "Provincia no encontrada o sin municipios"}, 404
    
    return municipios

@router.get("/municipios/{id_municipio}", response=MunicipioSchema)
def obtener_municipio(request, id_municipio: str):
    """Devuelve los datos de un municipio específico"""
    municipio = get_municipio(id_municipio)
    if not municipio:
        return {"detail": "Municipio no encontrado"}, 404
    
    return {
        "id": id_municipio,
        **municipio
    }