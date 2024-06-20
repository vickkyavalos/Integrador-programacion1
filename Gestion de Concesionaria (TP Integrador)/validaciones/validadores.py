import re

def transformarPatente(patente):
    return patente.upper()

def transformarEstado(estado):
    return estado.capitalize()

def validarPlaca(placa):
    return bool(re.match(r'^[A-Z]{3}[0-9]{3}$', placa))

def validarMarcaModelo(entrada):
    return bool(re.match(r'^[a-zA-Z\s]+$', entrada))

def validarTipoVehiculo(tipo):
    tipos_validos = ['Sedán', 'SUV', 'Pick Up', 'Camioneta', 'Hatchback', 'Coupé', 'Convertible', 'Hibrido', 'Desconocido']
    return tipo in tipos_validos

def validarAnio(anio):
    return anio.isdigit() and 1886 <= int(anio) <= 2024

def validarKilometraje(kilometraje):
    return kilometraje.isdigit() and int(kilometraje) >= 0

def validarPrecio(precio):
    try:
        return float(precio) >= 0
    except ValueError:
        return False

def validarEstado(estado):
    estados_validos = ['Disponible', 'Reservado', 'Vendido']
    return estado in estados_validos
