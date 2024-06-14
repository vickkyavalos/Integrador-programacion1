class Transaction:
    def __init__(self, transaccionId, customerId, vehiculoId, precioVenta):
        self.id = transaccionId
        self.customerId = customerId
        self.vehiculoId = vehiculoId
        self.precioVenta = precioVenta

    def a_dict(self):
        return {
            'id': self.id,
            'customerId': self.customerId,
            'vehiculoId': self.vehiculoId,
            'precioVenta': self.precioVenta
        }
