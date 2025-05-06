# apps/locations/schemas.py
from ninja import Schema
from typing import Dict, List, Optional

class ProvinciaSchema(Schema):
    """Schema para representar una provincia"""
    id: str
    nombre: str

class MunicipioSchema(Schema):
    """Schema para representar un municipio"""
    id: str
    nombre: str
    provincia_id: str
    provincia_nombre: str

class MunicipioSimpleSchema(Schema):
    """Schema para representar un municipio simple (sin provincia)"""
    id: str
    nombre: str

class ProvinciaConMunicipiosSchema(Schema):
    """Schema para representar una provincia con sus municipios"""
    id: str
    nombre: str
    municipios: Dict[str, str]