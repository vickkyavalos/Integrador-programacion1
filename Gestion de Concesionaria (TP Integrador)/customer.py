class Customer:
    def __init__(self, customerId, nombre, documento, apellido, direccion, celular, email):
        self.id = customerId
        self.nombre = nombre
        self.documento = documento
        self.apellido = apellido
        self.direccion = direccion
        self.celular = celular
        self.email = email

    def a_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'documento': self.documento,
            'apellido': self.apellido,
            'direccion': self.direccion,
            'celular': self.celular,
            'email': self.email
        }
