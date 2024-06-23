import json
import os

class Database:
    def __init__(self, rutaDeArchivo):
        self.rutaDeArchivo = rutaDeArchivo
        self.data = self.cargarData()

    #FUNCION NUEVA PARA LA CARGA DE DATOS DE LOS JSON
    def cargarData(self):
        if os.path.exists(self.rutaDeArchivo):
            try:
                with open(self.rutaDeArchivo, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    # Convertir campos numéricos de string a int o float si es necesario
                    for vehiculo in data:
                        vehiculo['anio'] = int(vehiculo['anio']) if 'anio' in vehiculo and isinstance(vehiculo['anio'], (int, str)) else None
                        vehiculo['precioVenta'] = float(vehiculo['precioVenta']) if 'precioVenta' in vehiculo and isinstance(vehiculo['precioVenta'], (float, int, str)) else None
                    return data
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error al cargar datos JSON: {e}")
                return []  # Archivo está vacío o no es un JSON válido
        else:
            return []
        
    #FUNCION ANTIGUA PARA CARGAR DATOS DE LOS JSON
    """def cargarData(self):
        if os.path.exists(self.rutaDeArchivo):
            try:
                with open(self.rutaDeArchivo, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []  # Archivo está vacío o no es un JSON válido
        else:
            return []"""

    def guardarData(self):
        with open(self.rutaDeArchivo, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)

    def agregarRegistro(self, registro):
        self.data.append(registro)
        self.guardarData()

    def actualizarRegistro(self, registroId, actualizarRegistro):
        for idx, registro in enumerate(self.data):
            if registro.get('id') == registroId:
                self.data[idx] = actualizarRegistro
                self.guardarData()
                return
        raise ValueError("Registro no disponible")

    def eliminarRegistro(self, registroId):
        self.data = [registro for registro in self.data if registro.get('id') != registroId]
        self.guardarData()

    def obtenerTodosLosRegistros(self):
        return self.data

    def buscarRegistrosPorId(self, registroId):
        for registro in self.data:
            if registro.get('id') == registroId:
                return registro
        return None
    
    def obtenerSiguienteId(self):
        if not self.data:
            return 1
        ultimoId = max(registro['id'] for registro in self.data)
        return ultimoId + 1
    

    #PARTE DE BUSQUEDA AVANZADA DE VEHICULOS
    ########################################
    def buscarPorMarca(self, marca):
        return [vehiculo for vehiculo in self.data if vehiculo.get('marca').lower() == marca.lower()]

    def buscarPorEstado(self, estado):
        return [vehiculo for vehiculo in self.data if vehiculo.get('estado').lower() == estado.lower()]

    def buscarPorRangoDePrecio(self, precio_min, precio_max, estado=None):
        resultados = []
        placas_vistas = set()

        for vehiculo in self.data:
            placa = vehiculo.get('placa')
            precio_venta = vehiculo.get('precioVenta')
            estado_vehiculo = vehiculo.get('estado')

            # Validamos si el vehículo cumple con los criterios de búsqueda
            if isinstance(precio_venta, (int, float)) and precio_min <= precio_venta <= precio_max:
                if estado is None or estado_vehiculo == estado:
                    # Verificamos si ya hemos visto este vehículo por su placa
                    if placa not in placas_vistas:
                        # Agregamos el vehículo a resultados y lo marcamos como visto
                        resultados.append(vehiculo)
                        placas_vistas.add(placa)
                    else:
                        # Si ya lo hemos visto, intentamos actualizar la información si falta
                        for index, existing in enumerate(resultados):
                            if existing.get('placa') == placa:
                                # Actualizamos año si falta
                                if existing.get('anio') is None and vehiculo.get('anio') is not None:
                                    resultados[index]['anio'] = vehiculo['anio']
                                # Actualizamos precio si falta
                                if existing.get('precioVenta') is None and vehiculo.get('precioVenta') is not None:
                                    resultados[index]['precioVenta'] = vehiculo['precioVenta']
                                break
            else:
                # Si el vehículo no cumple con los criterios de precio, revisamos si necesitamos actualizar la información
                for index, existing in enumerate(resultados):
                    if existing.get('placa') == placa:
                        # Actualizamos año si falta
                        if existing.get('anio') is None and vehiculo.get('anio') is not None:
                            resultados[index]['anio'] = vehiculo['anio']
                        # Actualizamos precio si falta
                        if existing.get('precioVenta') is None and vehiculo.get('precioVenta') is not None:
                            resultados[index]['precioVenta'] = vehiculo['precioVenta']
                        break

        return resultados

    def buscarPorRangoDePrecioYEstado(self, precio_min, precio_max, estado):
        return [vehiculo for vehiculo in self.data if precio_min <= vehiculo.get('precio', 0) <= precio_max and vehiculo.get('estado').lower() == estado.lower()]
    

    #PARTE DE BUSQUEDA AVANZADA DE CLIENTES
    #######################################
    def buscarPorNombre(self, nombre):
        resultados = []
        for cliente in self.data:
            if nombre.lower() in cliente.get('nombre', '').lower() or nombre.lower() in cliente.get('apellido', '').lower():
                resultados.append(cliente)
        return resultados
    
    def buscarPorDNI(self, dni):
        resultados = []
        for cliente in self.data:
            if cliente.get('documento') == dni:
                resultados.append(cliente)
        return resultados
    


    #PARTE DE BUSQUEDA AVANZADA DE TRANSACCIONES
    ############################################
    def buscarPorTipoTransaccion(self, tipo):
        resultados = [transaccion for transaccion in self.data if transaccion.get('tipo_transaccion') == tipo]
        return resultados

    def buscarPorRangoFecha(self, fecha_inicio, fecha_fin):
        resultados = []
        for transaccion in self.data:
            fecha_transaccion = transaccion.get('fecha')
            if fecha_inicio <= fecha_transaccion <= fecha_fin:
                resultados.append(transaccion)
        return resultados

    def buscarPorRangoMonto(self, monto_min, monto_max):
        resultados = [transaccion for transaccion in self.data if monto_min <= transaccion.get('monto', 0) <= monto_max]
        return resultados

    def buscarPorIDVehiculo(self, id_vehiculo):
        resultados = [transaccion for transaccion in self.data if transaccion.get('id_vehiculo') == id_vehiculo]
        return resultados

    def buscarPorIDCliente(self, id_cliente):
        resultados = [transaccion for transaccion in self.data if transaccion.get('id_cliente') == id_cliente]
        return resultados