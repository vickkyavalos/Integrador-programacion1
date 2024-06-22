import os
import platform
import sys
from vehicle import Vehicle
from customer import Customer
from transaction import Transaction
from database import Database
from validaciones import validadores
from validaciones import validadoresClientes



class InterfazConcesionario:
    def __init__(self):
        self.vehiculosDb = Database('data/vehiculos.json')
        self.customDb = Database('data/clientes.json')
        self.transaccionesDb = Database('data/transacciones.json')

    # Funcion para validar entradas (Metodo)
    def VerificacionDeEntrada(self, mensaje, valor_por_defecto, funcion_de_validacion, mensaje_de_error, funcDeTransformacion=None):
        while True:
            entrada = input(mensaje)
            if entrada == "":
                if valor_por_defecto is None:
                    return None
                else:
                    entrada = valor_por_defecto
            try:
                if funcDeTransformacion:
                    entrada = funcDeTransformacion(entrada)
                if funcion_de_validacion(entrada):
                    return entrada
                else:
                    print(mensaje_de_error)
            except ValueError:
                print(mensaje_de_error)

    def limpiar_consola(self):
        # Función para limpiar la consola según el sistema operativo
        if platform.system() == "Windows":
            os.system("cls")  # Comando para limpiar la consola en Windows
        else:
            os.system("clear")  # Comando para limpiar la consola en sistemas Unix (Linux, macOS, etc.)

    #Inicio del main menu
    def mainMenu(self):
        while True:
            print("\n1. Gestionar Vehiculos")
            print("2. Gestionar Clientes")
            print("3. Registrar Transaccion")
            print("4. Busqueda avanzada de vehiculos")
            print("5. Salir")
            choice = self.VerificacionDeEntrada("Seleccione una opción (1-5): ", None, lambda x: x in ["1", "2", "3", "4", "5"], "Opción inválida.")
            if choice == '1':
                self.modificarVehiculos()
            elif choice == '2':
                self.administrarCustomers()
            elif choice == '3':
                self.administrarTransacciones()
            elif choice == '4':
                self.busquedaAvanzada()
            elif choice == '5':
                sys.exit()
            else:
                print("Opcion invalida, por favor intentelo nuevamente.")





    ##############################
    ##############################
    ##-Funciones para Vehiculos-##
    ##############################
    ##############################
    
    #Inicio de funciones para vehiculos
    def modificarVehiculos(self):
        self.limpiar_consola()
        while True:
            print("\n1. Crear Vehiculo")
            print("2. Editar Vehiculo")
            print("3. Eliminar Vehiculo")
            print("4. Listar Vehiculos")
            print("5. Volver al menu principal")
            choice = input("Seleccione una opcion: ")
            if choice == '1':
                self.crearVehiculo()
            elif choice == '2':
                self.editarVehiculo()
            elif choice == '3':
                self.eliminarVehiculo()
            elif choice == '4':
                self.listarVehiculos()
            elif choice == '5':
                return
            else:
                print("Opcion invalida, por favor intente nuevamente.")

    def crearVehiculo(self):
        self.limpiar_consola()
        # Solicitar datos y crear el vehiculo
        placa = self.VerificacionDeEntrada("Ingrese la patente del vehiculo (ABC123): ", "", validadores.validarPlaca, "Patente invalida.", funcDeTransformacion=validadores.transformarPatente)
        marca = self.VerificacionDeEntrada("Ingrese la marca del vehiculo: ", "", validadores.validarMarcaModelo, "Marca invalida.")
        modelo = self.VerificacionDeEntrada("Ingrese el modelo del vehiculo: ", "", validadores.validarMarcaModelo, "Modelo invalido.")
        tipoVehiculo = self.VerificacionDeEntrada("Ingrese el tipo del vehiculo (Sedán, SUV, Pick Up, etc): ", "", validadores.validarTipoVehiculo, "Tipo de vehiculo invalido.")
        anio = self.VerificacionDeEntrada("Ingrese el año del vehiculo: ", "", validadores.validarAnio, "Año invalido. Debe ser un número entre 1886 y 2024.")
        kilometraje = self.VerificacionDeEntrada("Ingrese el kilometraje del vehiculo: ", "", validadores.validarKilometraje, "Kilometraje invalido. Debe ser un número positivo.")
        precioCompra = self.VerificacionDeEntrada("Ingrese el precio de compra del vehiculo: ", "", validadores.validarPrecio, "Precio de compra invalido. Debe ser un número positivo.")
        precioVenta = self.VerificacionDeEntrada("Ingrese el precio de venta del vehiculo: ", "", validadores.validarPrecio, "Precio de venta invalido. Debe ser un número positivo.")
        estado = self.VerificacionDeEntrada("Ingrese el estado del vehiculo (Disponible, Reservado, Vendido): ", "", validadores.validarEstado, "Estado invalido.", funcDeTransformacion=validadores.transformarEstado)

        vehiculoId = self.vehiculosDb.obtenerSiguienteId()
        nuevoVehiculo = Vehicle(vehiculoId, placa, marca, modelo, tipoVehiculo, int(anio), int(kilometraje), float(precioCompra), float(precioVenta), estado)
        self.vehiculosDb.agregarRegistro(nuevoVehiculo.a_dict())
        print("Vehiculo creado correctamente.")

    def editarVehiculo(self):
        self.limpiar_consola()
        vehiculoId = int(input("Ingrese el ID del vehiculo a editar: "))
        vehiculo = self.vehiculosDb.buscarRegistrosPorId(vehiculoId)
        if vehiculo:
            print("Deje en blanco si no desea modificar el campo.")
            
            campos = {
                'placa': 'Placa',
                'marca': 'Marca',
                'modelo': 'Modelo',
                'tipoVehiculo': 'Tipo de vehiculo',
                'anio': 'Año',
                'kilometraje': 'Kilometraje',
                'precioCompra': 'Precio de compra',
                'precioVenta': 'Precio de venta',
                'estado': 'Estado'
            }
            
            valores_actualizados = {}
            for campo, descripcion in campos.items():
                valor_actual = vehiculo.get(campo, 'N/A')
                nuevo_valor = input(f"{descripcion} actual ({valor_actual}): ") or valor_actual
                valores_actualizados[campo] = nuevo_valor

            # Convertir los valores que necesitan ser numéricos
            valores_actualizados['anio'] = int(valores_actualizados['anio'])
            valores_actualizados['kilometraje'] = int(valores_actualizados['kilometraje'])
            valores_actualizados['precioCompra'] = float(valores_actualizados['precioCompra'])
            valores_actualizados['precioVenta'] = float(valores_actualizados['precioVenta'])

            actualizarVehiculo = Vehicle(
                vehiculoId,
                valores_actualizados['placa'],
                valores_actualizados['marca'],
                valores_actualizados['modelo'],
                valores_actualizados['tipoVehiculo'],
                valores_actualizados['anio'],
                valores_actualizados['kilometraje'],
                valores_actualizados['precioCompra'],
                valores_actualizados['precioVenta'],
                valores_actualizados['estado']
            )
            self.vehiculosDb.actualizarRegistro(vehiculoId, actualizarVehiculo.a_dict())
            print("Vehiculo actualizado exitosamente.")
        else:
            print("Vehiculo no encontrado.")

    def eliminarVehiculo(self):
        self.limpiar_consola()
        # Solicitar ID del vehiculo y eliminarlo
        vehiculoId = int(input("Ingrese el ID del vehiculo a eliminar: "))
        self.vehiculosDb.eliminarRegistro(vehiculoId)
        print("Vehiculo eliminado exitosamente.")

    def listarVehiculos(self):
        self.limpiar_consola()
        vehiculos = self.vehiculosDb.obtenerTodosLosRegistros()
        if vehiculos:
            print("{:<5} {:<10} {:<10} {:<10} {:<15} {:<5} {:<12} {:<15} {:<15}".format(
                "ID", "Placa", "Marca", "Modelo", "Tipo", "Año", "Kilometraje", "Precio Compra", "Precio Venta"
            ))
            print("=" * 100)
            for vehiculo in vehiculos:
                print("{:<5} {:<10} {:<10} {:<10} {:<15} {:<5} {:<12} {:<15} {:<15}".format(
                    vehiculo.get('id', 'N/A'),
                    vehiculo.get('placa', 'N/A'),
                    vehiculo.get('marca', 'N/A'),
                    vehiculo.get('modelo', 'N/A'),
                    vehiculo.get('tipoVehiculo', 'N/A'),
                    vehiculo.get('anio', 'N/A'),
                    vehiculo.get('kilometraje', 'N/A'),
                    vehiculo.get('precioCompra', 'N/A'),
                    vehiculo.get('precioVenta', 'N/A')
                ))
        else:
            print("No hay vehiculos registrados.")
    #Fin de funciones para vehiculos

    



    ###############################
    ###############################
    ###-Funciones para Clientes-###
    ###############################
    ###############################

    def administrarCustomers(self):
        self.limpiar_consola()
        # similar a modificarVehiculos
        while True:
            print("\n1. Crear Cliente")
            print("2. Editar Cliente")
            print("3. Eliminar Cliente")
            print("4. Listar Clientes")
            print("5. Volver al Menu Principal")
            choice = input("Seleccione una opcion: ")
            if choice == '1':
                self.crearCustomer()
            elif choice == '2':
                self.editarCustomer()
            elif choice == '3':
                self.eliminarCustomer()
            elif choice == '4':
                self.listarClientes()
            elif choice == '5':
                return
            else:
                print("Opcion invalida, por favor intente nuevamente.")

    def crearCustomer(self):
        self.limpiar_consola()
        nombre = self.VerificacionDeEntrada("Ingrese el nombre del cliente: ", "", validadoresClientes.validarNombre, "Nombre invalido. Solo se permiten letras.")
        documento = self.VerificacionDeEntrada("Ingrese el documento del cliente: ", "", validadoresClientes.validarDocumento, "Documento invalido. Debe ser un número de 7, 8 o 9 dígitos.")
        apellido = self.VerificacionDeEntrada("Ingrese el apellido del cliente: ", "", validadoresClientes.validarApellido, "Apellido invalido. Solo se permiten letras.")
        direccion = self.VerificacionDeEntrada("Ingrese la direccion del cliente: ", "", validadoresClientes.validarDireccion, "Direccion invalida.")
        celular = self.VerificacionDeEntrada("Ingrese el telefono del cliente: ", "", validadoresClientes.validarCelular, "Telefono invalido. Debe ser un número de 10 o 11 dígitos.")
        email = self.VerificacionDeEntrada("Ingrese el correo electronico del cliente: ", "", validadoresClientes.validarEmail, "Correo electronico invalido.")

        customerId = self.customDb.obtenerSiguienteId()
        nuevoCustomer = Customer(customerId, nombre, documento, apellido, direccion, celular, email)
        self.customDb.agregarRegistro(nuevoCustomer.a_dict())
        print("Cliente creado exitosamente.")

    def listarClientes(self):
        self.limpiar_consola()
        # Mostrar todos los clientes en formato de tabla
        clientes = self.customDb.obtenerTodosLosRegistros()
        if clientes:
            # Obtener la longitud máxima de los datos para cada columna
            max_lengths = {
                "ID": max(len(str(cliente.get('id', 'N/A'))) for cliente in clientes),
                "Nombre": max(len(cliente.get('nombre', 'N/A')) for cliente in clientes),
                "Documento": max(len(str(cliente.get('documento', 'N/A'))) for cliente in clientes),
                "Apellido": max(len(cliente.get('apellido', 'N/A')) for cliente in clientes),
                "Direccion": max(len(cliente.get('direccion', 'N/A')) for cliente in clientes),
                "Celular": max(len(cliente.get('celular', 'N/A')) for cliente in clientes),
                "Email": max(len(cliente.get('email', 'N/A')) for cliente in clientes),
            }

            # Imprime los encabezados de las columnas
            print("{:<{id_width}} {:<{nombre_width}} {:<{doc_width}} {:<{apellido_width}} {:<{direccion_width}} {:<{celular_width}} {:<{email_width}}".format(
                "ID", "Nombre", "Documento", "Apellido", "Direccion", "Celular", "Email",
                id_width=max_lengths["ID"] + 2, nombre_width=max_lengths["Nombre"] + 2,
                doc_width=max_lengths["Documento"] + 2, apellido_width=max_lengths["Apellido"] + 2,
                direccion_width=max_lengths["Direccion"] + 2, celular_width=max_lengths["Celular"] + 2,
                email_width=max_lengths["Email"] + 2  # Agregar +2 para la columna de email también
            ))

            # Calcular la longitud de la línea divisoria
            total_width = (
                max_lengths["ID"] + 2 +
                max_lengths["Nombre"] + 2 +
                max_lengths["Documento"] + 2 +
                max_lengths["Apellido"] + 2 +
                max_lengths["Direccion"] + 2 +
                max_lengths["Celular"] + 2 +
                max_lengths["Email"] + 2  # Incluir la longitud de la columna de email
            )
            print("=" * total_width)  # Línea divisoria

            # Imprime los datos de los clientes
            for cliente in clientes:
                print("{:<{id_width}} {:<{nombre_width}} {:<{doc_width}} {:<{apellido_width}} {:<{direccion_width}} {:<{celular_width}} {:<{email_width}}".format(
                    cliente.get('id', 'N/A'),
                    cliente.get('nombre', 'N/A'),
                    cliente.get('documento', 'N/A'),
                    cliente.get('apellido', 'N/A'),
                    cliente.get('direccion', 'N/A'),
                    cliente.get('celular', 'N/A'),
                    cliente.get('email', 'N/A'),
                    id_width=max_lengths["ID"] + 2, nombre_width=max_lengths["Nombre"] + 2,
                    doc_width=max_lengths["Documento"] + 2, apellido_width=max_lengths["Apellido"] + 2,
                    direccion_width=max_lengths["Direccion"] + 2, celular_width=max_lengths["Celular"] + 2,
                    email_width=max_lengths["Email"] + 2  # Agregar +2 para la columna de email también
                ))
        else:
            print("No hay clientes registrados.")

    def editarCustomer(self):
        #self.limpiar_consola() FRAGMENTO PARA LIMPIAR CONSOLA
        customerId = int(input("Ingrese el ID del cliente a editar: "))
        customer = self.customDb.buscarRegistrosPorId(customerId)
        if customer:
            print("Deje en blanco si no desea modificar el campo.")

            nombre = self.VerificacionDeEntrada(
                f"Nombre actual ({customer['nombre']}): ",
                customer['nombre'],
                validadoresClientes.validarNombre,
                "Nombre invalido. Solo se permiten letras."
            )

            documento = self.VerificacionDeEntrada(
                f"Documento actual ({customer['documento']}): ",
                customer['documento'],
                validadoresClientes.validarDocumento,
                "Documento invalido. Debe ser un número de 7, 8 o 9 dígitos."
            )

            apellido = self.VerificacionDeEntrada(
                f"Apellido actual ({customer['apellido']}): ",
                customer['apellido'],
                validadoresClientes.validarApellido,
                "Apellido invalido. Solo se permiten letras."
            )

            direccion = self.VerificacionDeEntrada(
                f"Direccion actual ({customer['direccion']}): ",
                customer['direccion'],
                validadoresClientes.validarDireccion,
                "Direccion invalida."
            )

            celular = self.VerificacionDeEntrada(
                f"Telefono actual ({customer['celular']}): ",
                customer['celular'],
                validadoresClientes.validarCelular,
                "Telefono invalido. Debe ser un número de 10 o 11 dígitos."
            )

            email = self.VerificacionDeEntrada(
                f"Correo electronico actual ({customer['email']}): ",
                customer['email'],
                validadoresClientes.validarEmail,
                "Correo electronico invalido."
            )

            actualizarCustomer = Customer(customerId, nombre, documento, apellido, direccion, celular, email)
            self.customDb.actualizarRegistro(customerId, actualizarCustomer.a_dict())
            print("Cliente actualizado exitosamente.")
        else:
            print("Cliente no encontrado.")

    def eliminarCustomer(self):
        self.limpiar_consola()
        customerId = int(input("Ingrese el ID del cliente a eliminar: "))
        self.customDb.eliminarRegistro(customerId)
        print("Cliente eliminado exitosamente.")
    #Fin de funciones para customers





    ##############################
    ##############################
    #Funciones para Transacciones#
    ##############################
    ##############################

    #Inicio de funciones para transacciones
    def administrarTransacciones(self):
        self.limpiar_consola()
        while True:
            print("\n1. Crear Transaccion")
            print("2. Listar Transacciones")
            print("3. Volver al Menu Principal")
            choice = input("Seleccione una opcion: ")
            if choice == '1':
                self.crearTransaccion()
            elif choice == '2':
                self.listarTransacciones()
            elif choice == '3':
                return
            else:
                print("Opcion invalida, por favor intente nuevamente.")
    
    def crearTransaccion(self):
        try:
            self.limpiar_consola()

            id_transaccion = len(self.transaccionesDb.obtenerTodosLosRegistros()) + 1
            id_vehiculo = int(input("Ingrese el ID del vehículo: "))
            id_cliente = int(input("Ingrese el ID del cliente: "))
            tipo_transaccion = input("Ingrese el tipo de transacción (Venta/Compra): ")
            fecha = input("Ingrese la fecha de la transacción (YYYY-MM-DD): ")
            monto = float(input("Ingrese el monto de la transacción: "))
            observaciones = input("Ingrese observaciones sobre la transacción: ")

            nueva_transaccion = {
                "id_transaccion": id_transaccion,
                "id_vehiculo": id_vehiculo,
                "id_cliente": id_cliente,
                "tipo_transaccion": tipo_transaccion,
                "fecha": fecha,
                "monto": monto,
                "observaciones": observaciones
            }

            self.transaccionesDb.agregarRegistro(nueva_transaccion)
            print("Transacción creada exitosamente.")
        except ValueError as e:
            print(f"Error en la entrada de datos: {e}")
    
    def listarTransacciones(self):
        self.limpiar_consola()

        transacciones = self.transaccionesDb.obtenerTodosLosRegistros()
        if transacciones:
        # Calcular los anchos máximos de cada columna, incluyendo los encabezados
            max_lengths = {
            "ID_Transaccion": max(len("ID_Transaccion"), max(len(str(transaccion.get('id_transaccion', 'N/A'))) for transaccion in transacciones)),
            "ID_Vehiculo": max(len("ID_Vehiculo"), max(len(str(transaccion.get('id_vehiculo', 'N/A'))) for transaccion in transacciones)),
            "ID_Cliente": max(len("ID_Cliente"), max(len(str(transaccion.get('id_cliente', 'N/A'))) for transaccion in transacciones)),
            "Tipo_Transaccion": max(len("Tipo_Transaccion"), max(len(transaccion.get('tipo_transaccion', 'N/A')) for transaccion in transacciones)),
            "Fecha": max(len("Fecha"), max(len(transaccion.get('fecha', 'N/A')) for transaccion in transacciones)),
            "Monto": max(len("Monto"), max(len(str(transaccion.get('monto', 'N/A'))) for transaccion in transacciones)),
            "Observaciones": max(len("Observaciones"), max(len(transaccion.get('observaciones', 'N/A')) for transaccion in transacciones))
            }

            # Imprimir encabezados de la tabla
            print("{:<{id_width}} {:<{vehiculo_width}} {:<{cliente_width}} {:<{tipo_width}} {:<{fecha_width}} {:<{monto_width}} {:<{obs_width}}".format(
            "ID-T", "ID-V", "ID-C", "Transaccion", "Fecha", "Monto", "Observaciones",
            id_width=max_lengths["ID_Transaccion"], vehiculo_width=max_lengths["ID_Vehiculo"],
            cliente_width=max_lengths["ID_Cliente"], tipo_width=max_lengths["Tipo_Transaccion"],
            fecha_width=max_lengths["Fecha"], monto_width=max_lengths["Monto"],
            obs_width=max_lengths["Observaciones"]
            ))
            print("=" * (sum(max_lengths.values()) + len(max_lengths) * 2))

            # Imprimir cada transacción en formato de tabla
            for transaccion in transacciones:
                print("{:<{id_width}} {:<{vehiculo_width}} {:<{cliente_width}} {:<{tipo_width}} {:<{fecha_width}} {:<{monto_width}} {:<{obs_width}}".format(
                    transaccion.get('id_transaccion', 'N/A'),
                    transaccion.get('id_vehiculo', 'N/A'),
                    transaccion.get('id_cliente', 'N/A'),
                    transaccion.get('tipo_transaccion', 'N/A'),
                    transaccion.get('fecha', 'N/A'),
                    transaccion.get('monto', 'N/A'),
                    transaccion.get('observaciones', 'N/A'),
                    id_width=max_lengths["ID_Transaccion"], vehiculo_width=max_lengths["ID_Vehiculo"],
                    cliente_width=max_lengths["ID_Cliente"], tipo_width=max_lengths["Tipo_Transaccion"],
                    fecha_width=max_lengths["Fecha"], monto_width=max_lengths["Monto"],
                    obs_width=max_lengths["Observaciones"]
                ))
        else:
            print("No hay transacciones registradas.")  
    #Fin de funciones para transacciones


    #################################
    #FUNCIONES PARA BUSQUEDA AVANZADA
    #################################
    def mostrarVehiculos(self, vehiculos):
        if not vehiculos:
            print("No se encontraron vehículos.")
            return

    
    def busquedaAvanzada(self):
        while True:
            try: 
                print("\nOpciones de busqueda avanzada.")
                print("1. Buscar por marca")
                print("2. Buscar por estado (Disponible, Reservado, Vendido)")
                print("3. Buscar por rango de precio")
                print("4. Buscar por rango de precio y estado")
                print("5. Volver al menu principal")
                opcion = self.VerificacionDeEntrada("Seleccione una opcion (1-5): ", None, lambda x: x in ["1", "2", "3", "4", "5"], "Opcion invalida.")
                
                if opcion == "1":
                    marca = self.VerificacionDeEntrada("Ingrese la marca (deje en blanco para volver): ", None, lambda x: x == "" or x.isalpha(), "Marca invalida.")
                    if marca == "":
                        return #Volvemos al menu anterior
                    resultados = self.vehiculosDb.buscarPorMarca(marca)
                    self.mostrarVehiculos(resultados)
                
                elif opcion == "2":
                    estado = self.VerificacionDeEntrada("Ingrese el estado (Disponible, Reservado, Vendido) (deje en blanco para volver): ", None, lambda x: x == "" or x.lower() in ["disponible", "reservado", "vendido"], "Estado inválido.")
                    if estado == "":
                        return #Volver al menu anterior
                    resultados = self.vehiculosDb.buscarPorEstado(estado)
                    self.mostrarVehiculos(resultados)

                elif opcion == "3":
                    precioMinimo = self.VerificacionDeEntrada("Ingrese el precio minimo (deja en blanco para volver): ", None, lambda x: x == "" or x.isdigit(), "Precio mínimo inválido.")
                    if precioMinimo == "":
                        return #Volver al menu anterior
                    precioMaximo = self.VerificacionDeEntrada("Ingrese el precio maximo (deje en blanco para volver): ", None, lambda x: x == "" or x.isdigit(), "Precio máximo inválido.")
                    if precioMaximo == "":
                        return #Volver al menu anterior
                    resultados = self.vehiculosDb.buscarPorRangoDePrecio(int(precioMinimo), int(precioMaximo))
                    self.mostrarVehiculos(resultados)

                elif opcion == "4":
                    precio_min = self.VerificacionDeEntrada("Ingrese el precio mínimo (deje en blanco para volver): ", None, lambda x: x == "" or x.isdigit(), "Precio mínimo inválido.")
                    if precio_min == "":
                            return  # Volver al menú anterior
                    precio_max = self.VerificacionDeEntrada("Ingrese el precio máximo (deje en blanco para volver): ", None, lambda x: x == "" or x.isdigit(), "Precio máximo inválido.")
                    if precio_max == "":
                        return  # Volver al menú anterior
                    estado = self.VerificacionDeEntrada("Ingrese el estado (Disponible, Reservado, Vendido) (deje en blanco para volver): ", None, lambda x: x == "" or x.lower() in ["disponible", "reservado", "vendido"], "Estado inválido.")
                    if estado == "":
                        return  # Volver al menú anterior
                    resultados = self.vehiculosDb.buscarPorRangoDePrecio(int(precio_min), int(precio_max), estado)
                    self.mostrarVehiculos(resultados)

                elif opcion == "5":
                    return #Volver al menu principal
                
            except ValueError as e:
                print(f"Error en la entrada de datos: {e}")





if __name__ == "__main__":
    interface = InterfazConcesionario()
    interface.mainMenu()