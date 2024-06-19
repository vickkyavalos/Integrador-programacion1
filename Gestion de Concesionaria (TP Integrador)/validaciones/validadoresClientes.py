def validarNombre(nombre):
    return nombre.isalpha() and len(nombre) > 0

def validarDocumento(documento):
    return documento.isdigit() and len(documento) in (7, 8, 9)

def validarApellido(apellido):
    return apellido.isalpha() and len(apellido) > 0

def validarDireccion(direccion):
    return len(direccion) > 0

def validarCelular(celular):
    return celular.isdigit() and len(celular) in (10, 11)

def validarEmail(email):
    import re
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None