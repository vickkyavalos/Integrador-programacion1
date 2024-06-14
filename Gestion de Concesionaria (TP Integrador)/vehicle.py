class Vehicle:
    def __init__(self, vehiculoId, patente, marca, modelo, tipo, anio, kilometraje, precioCompra, precioVenta, estado):
        self.id = vehiculoId
        self.patente = patente
        self.marca = marca
        self.modelo = modelo
        self.tipo = tipo
        self.anio = anio
        self.kilometraje = kilometraje
        self.precioCompra = precioCompra
        self.precioVenta = precioVenta
        self.estado = estado

    def a_dict(self):
        return {
            'id': self.id,
            'placa': self.patente,
            'marca': self.marca,
            'modelo': self.modelo,
            'tipoVehiculo': self.tipo,
            'anio': self.anio,
            'kilometraje': self.kilometraje,
            'precioCompra': self.precioCompra,
            'precioVenta': self.precioVenta,
            'estado': self.estado
        }
