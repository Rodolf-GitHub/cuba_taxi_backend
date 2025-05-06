# apps/locations/data.py

# Estructura de datos:
# {
#     "id_provincia": {
#         "nombre": "Nombre de Provincia",
#         "municipios": {
#             "id_municipio": "Nombre de Municipio",
#             ...
#         }
#     },
#     ...
# }

PROVINCIAS_MUNICIPIOS = {
    "01": {
        "nombre": "Pinar del Río",
        "municipios": {
            "0101": "Pinar del Río",
            "0102": "Sandino",
            "0103": "Mantua",
            "0104": "Minas de Matahambre",
            "0105": "Viñales",
            "0106": "La Palma",
            "0107": "Los Palacios",
            "0108": "Consolación del Sur",
            "0109": "San Luis",
            "0110": "San Juan y Martínez",
            "0111": "Guane"
        }
    },
    "02": {
        "nombre": "Artemisa",
        "municipios": {
            "0201": "Artemisa",
            "0202": "Bahía Honda",
            "0203": "Candelaria",
            "0204": "San Cristóbal",
            "0205": "Mariel",
            "0206": "Guanajay",
            "0207": "Caimito",
            "0208": "Bauta",
            "0209": "San Antonio de los Baños",
            "0210": "Güira de Melena",
            "0211": "Alquízar"
        }
    },
    "03": {
        "nombre": "La Habana",
        "municipios": {
            "0301": "Playa",
            "0302": "Plaza de la Revolución",
            "0303": "Centro Habana",
            "0304": "La Habana Vieja",
            "0305": "Regla",
            "0306": "La Habana del Este",
            "0307": "Guanabacoa",
            "0308": "San Miguel del Padrón",
            "0309": "Diez de Octubre",
            "0310": "Cerro",
            "0311": "Marianao",
            "0312": "La Lisa",
            "0313": "Boyeros",
            "0314": "Arroyo Naranjo",
            "0315": "Cotorro"
        }
    },
    "04": {
        "nombre": "Mayabeque",
        "municipios": {
            "0401": "San José de las Lajas",
            "0402": "Jaruco",
            "0403": "Santa Cruz del Norte",
            "0404": "Madruga",
            "0405": "Nueva Paz",
            "0406": "San Nicolás",
            "0407": "Güines",
            "0408": "Melena del Sur",
            "0409": "Batabanó",
            "0410": "Quivicán",
            "0411": "Bejucal"
        }
    },
    "05": {
        "nombre": "Matanzas",
        "municipios": {
            "0501": "Matanzas",
            "0502": "Cárdenas",
            "0503": "Martí",
            "0504": "Colón",
            "0505": "Perico",
            "0506": "Jovellanos",
            "0507": "Pedro Betancourt",
            "0508": "Limonar",
            "0509": "Unión de Reyes",
            "0510": "Ciénaga de Zapata",
            "0511": "Jagüey Grande",
            "0512": "Calimete",
            "0513": "Los Arabos"
        }
    },
    "06": {
        "nombre": "Cienfuegos",
        "municipios": {
            "0601": "Cienfuegos",
            "0602": "Abreus",
            "0603": "Aguada de Pasajeros",
            "0604": "Rodas",
            "0605": "Palmira",
            "0606": "Lajas",
            "0607": "Cruces",
            "0608": "Cumanayagua"
        }
    },
    "07": {
        "nombre": "Villa Clara",
        "municipios": {
            "0701": "Santa Clara",
            "0702": "Corralillo",
            "0703": "Quemado de Güines",
            "0704": "Sagua la Grande",
            "0705": "Encrucijada",
            "0706": "Camajuaní",
            "0707": "Caibarién",
            "0708": "Remedios",
            "0709": "Placetas",
            "0710": "Santa Clara",
            "0711": "Cifuentes",
            "0712": "Santo Domingo",
            "0713": "Ranchuelo",
            "0714": "Manicaragua"
        }
    },
    "08": {
        "nombre": "Sancti Spíritus",
        "municipios": {
            "0801": "Sancti Spíritus",
            "0802": "Yaguajay",
            "0803": "Jatibonico",
            "0804": "Taguasco",
            "0805": "Cabaiguán",
            "0806": "Fomento",
            "0807": "Trinidad",
            "0808": "La Sierpe"
        }
    },
    "09": {
        "nombre": "Ciego de Ávila",
        "municipios": {
            "0901": "Ciego de Ávila",
            "0902": "Chambas",
            "0903": "Morón",
            "0904": "Bolivia",
            "0905": "Primero de Enero",
            "0906": "Ciro Redondo",
            "0907": "Florencia",
            "0908": "Majagua",
            "0909": "Baraguá",
            "0910": "Venezuela"
        }
    },
    "10": {
        "nombre": "Camagüey",
        "municipios": {
            "1001": "Camagüey",
            "1002": "Carlos Manuel de Céspedes",
            "1003": "Esmeralda",
            "1004": "Sierra de Cubitas",
            "1005": "Minas",
            "1006": "Nuevitas",
            "1007": "Guáimaro",
            "1008": "Sibanicú",
            "1009": "Camagüey",
            "1010": "Florida",
            "1011": "Vertientes",
            "1012": "Jimaguayú",
            "1013": "Najasa",
            "1014": "Santa Cruz del Sur"
        }
    },
    "11": {
        "nombre": "Las Tunas",
        "municipios": {
            "1101": "Las Tunas",
            "1102": "Manatí",
            "1103": "Puerto Padre",
            "1104": "Jesús Menéndez",
            "1105": "Majibacoa",
            "1106": "Las Tunas",
            "1107": "Jobabo",
            "1108": "Colombia"
        }
    },
    "12": {
        "nombre": "Granma",
        "municipios": {
            "1201": "Río Cauto",
            "1202": "Cauto Cristo",
            "1203": "Jiguaní",
            "1204": "Bayamo",
            "1205": "Yara",
            "1206": "Manzanillo",
            "1207": "Campechuela",
            "1208": "Media Luna",
            "1209": "Niquero",
            "1210": "Pilón",
            "1211": "Bartolomé Masó",
            "1212": "Bayamo",
            "1213": "Guisa"
        }
    },
    "13": {
        "nombre": "Holguín",
        "municipios": {
            "1301": "Gibara",
            "1302": "Rafael Freyre",
            "1303": "Banes",
            "1304": "Antilla",
            "1305": "Báguanos",
            "1306": "Holguín",
            "1307": "Calixto García",
            "1308": "Cacocum",
            "1309": "Urbano Noris",
            "1310": "Cueto",
            "1311": "Mayarí",
            "1312": "Frank País",
            "1313": "Sagua de Tánamo",
            "1314": "Moa"
        }
    },
    "14": {
        "nombre": "Santiago de Cuba",
        "municipios": {
            "1401": "Contramaestre",
            "1402": "Mella",
            "1403": "San Luis",
            "1404": "Segundo Frente",
            "1405": "Songo-La Maya",
            "1406": "Santiago de Cuba",
            "1407": "Palma Soriano",
            "1408": "Tercer Frente",
            "1409": "Guamá"
        }
    },
    "15": {
        "nombre": "Guantánamo",
        "municipios": {
            "1501": "El Salvador",
            "1502": "Guantánamo",
            "1503": "Yateras",
            "1504": "Baracoa",
            "1505": "Maisí",
            "1506": "Imías",
            "1507": "San Antonio del Sur",
            "1508": "Manuel Tames",
            "1509": "Caimanera",
            "1510": "Niceto Pérez"
        }
    },
    "16": {
        "nombre": "Isla de la Juventud",
        "municipios": {
            "1601": "Isla de la Juventud"
        }
    }
}

def get_all_provincias():
    """Devuelve todas las provincias con sus IDs"""
    return {id_prov: data["nombre"] for id_prov, data in PROVINCIAS_MUNICIPIOS.items()}

def get_provincia(id_provincia):
    """Devuelve los datos de una provincia específica"""
    return PROVINCIAS_MUNICIPIOS.get(id_provincia)

def get_all_municipios():
    """Devuelve todos los municipios con sus IDs"""
    all_municipios = {}
    for id_prov, data in PROVINCIAS_MUNICIPIOS.items():
        for id_mun, nombre in data["municipios"].items():
            all_municipios[id_mun] = {
                "nombre": nombre,
                "provincia_id": id_prov,
                "provincia_nombre": data["nombre"]
            }
    return all_municipios

def get_municipios_by_provincia(id_provincia):
    """Devuelve los municipios de una provincia específica"""
    provincia = PROVINCIAS_MUNICIPIOS.get(id_provincia)
    if provincia:
        return provincia["municipios"]
    return {}

def get_municipio(id_municipio):
    """Devuelve los datos de un municipio específico"""
    all_municipios = get_all_municipios()
    return all_municipios.get(id_municipio)