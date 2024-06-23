import os
import platform
import sys
from vehicle import Vehicle
from customer import Customer
from transaction import Transaction
from database import Database
from validaciones import validadores
from validaciones import validadoresClientes
from rich.console import Console  #Para la interffaz
from rich.panel import Panel
from rich import print
from rich.table import Table
from rich.panel import Panel

console = Console()

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

        console = Console()
        
        panel = Panel("Sistema de Gestión de Concesionaria de Vehículos Usados", style="bold magenta", padding=(1, 2),
        expand=True)
        console.print(panel, justify="center")

        while True:
            
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Opción", style="dim", width=12)
            table.add_column("Descripción")
            table.add_row("1", "Gestionar Vehículos")
            table.add_row("2", "Gestionar Clientes")
            table.add_row("3", "Registrar Transacción")
            table.add_row("4", "Busqueda avanzada de vehiculos") 
            table.add_row("5", "Salir")
            console.print(table)

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
                console.print("Saliendo del sistema... [bold red]¡Adiós![/bold red]", style="bold yellow")
                sys.exit()
            else:
                console.print("Opción inválida, por favor inténtelo nuevamente.", style="bold red")


    ##############################
    ##############################
    ##-Funciones para Vehiculos-##
    ##############################
    ##############################
    
    #Inicio de funciones para vehiculos
    def modificarVehiculos(self):
        
        self.limpiar_consola()
        while True:

            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Opción", style="dim", width=12)
            table.add_column("Descripción")
            table.add_row("1", "Crear Vehiculo")
            table.add_row("2", "Editar Vehiculo")
            table.add_row("3", "Eliminar Vehiculo")
            table.add_row("4", "Listar Vehiculos") 
            table.add_row("5", "Volver al menu principal")
            console.print(table)
           
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
                console.print("Opcion invalida, por favor intente nuevamente.", style="bold red")

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
        console.print("Vehiculo creado correctamente.",style="bold green")

    def editarVehiculo(self):
        self.limpiar_consola()
        vehiculoId = int(input("Ingrese el ID del vehiculo a editar: "))
        vehiculo = self.vehiculosDb.buscarRegistrosPorId(vehiculoId)
        if vehiculo:
            print(Panel("Deje en blanco si no desea modificar el campo."))
            
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
            console.print("Vehiculo actualizado exitosamente.",style="bold green")
        else:
            console.print("Vehiculo no encontrado.",style="bold red")

    def eliminarVehiculo(self):

        console = Console()

        self.limpiar_consola()
        # Solicitar ID del vehiculo y eliminarlo
        vehiculoId = int(input("Ingrese el ID del vehiculo a eliminar: "))
        self.vehiculosDb.eliminarRegistro(vehiculoId)
        console.print("Vehiculo eliminado exitosamente.",style="bold green")

    def listarVehiculos(self):
        self.limpiar_consola()

        vehiculos = self.vehiculosDb.obtenerTodosLosRegistros()
        if vehiculos:
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("ID", style="dim", width=5)
            table.add_column("Placa", style="dim", width=10)
            table.add_column("Marca", style="dim", width=10)
            table.add_column("Modelo", style="dim", width=10)
            table.add_column("Tipo", style="dim", width=15)
            table.add_column("Año", style="dim", width=5)
            table.add_column("Kilometraje", style="dim", width=12)
            table.add_column("Precio Compra", style="dim", width=15, justify="right")
            table.add_column("Precio Venta", style="dim", width=15, justify="right")
            
            for vehiculo in vehiculos:
                table.add_row(
                    str(vehiculo.get('id', 'N/A')),
                    vehiculo.get('placa', 'N/A'),
                    vehiculo.get('marca', 'N/A'),
                    vehiculo.get('modelo', 'N/A'),
                    vehiculo.get('tipoVehiculo', 'N/A'),
                    str(vehiculo.get('anio', 'N/A')),
                    str(vehiculo.get('kilometraje', 'N/A')),
                    f"${vehiculo.get('precioCompra', 'N/A')}",
                    f"${vehiculo.get('precioVenta', 'N/A')}"
            )
            console.print(table)
        else:
            console.print("No hay vehiculos registrados.", style="bold red")

    ###############################
    ###############################
    ###-Funciones para Clientes-###
    ###############################
    ###############################

    def administrarCustomers(self):
        self.limpiar_consola()
        # similar a modificarVehiculos
        while True:

            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Opción", style="dim", width=12)
            table.add_column("Descripción")
            table.add_row("1", "Crear Cliente")
            table.add_row("2", "Editar Cliente")
            table.add_row("3", "Eliminar Cliente")
            table.add_row("4", "Listar Clientes") 
            table.add_row("5", "Volver al Menu Principal")
            console.print(table)

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
                print("Opcion invalida, por favor intente nuevamente.", style= "bold red")

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
        console.print("Cliente creado exitosamente.", style="bold green")

    def listarClientes(self):
        console = Console()
        self.limpiar_consola()
        clientes = self.customDb.obtenerTodosLosRegistros() 
        if clientes:
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("ID", style="dim", width=5)
            table.add_column("Nombre", style="dim", width=10)
            table.add_column("Documento", style="dim", width=12)
            table.add_column("Apellido", style="dim", width=15)
            table.add_column("Dirección", style="dim", width=20)
            table.add_column("Celular", style="dim", width=12)
            table.add_column("Email", style="dim", width=25)

            for cliente in clientes:
                table.add_row(
                    str(cliente.get('id', 'N/A')),
                    cliente.get('nombre', 'N/A'),
                    cliente.get('documento', 'N/A'),
                    cliente.get('apellido', 'N/A'),
                    cliente.get('direccion', 'N/A'),
                    cliente.get('celular', 'N/A'),
                    cliente.get('email', 'N/A')
                )

            console.print(table)
        else:
            console.print("No hay clientes registrados.", style="bold red")


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
            console.print("Cliente actualizado exitosamente.",style="bold green")
        else:
            console.print("Cliente no encontrado.",style="bold red")

    def eliminarCustomer(self):
        self.limpiar_consola()
        customerId = int(input("Ingrese el ID del cliente a eliminar: "))
        self.customDb.eliminarRegistro(customerId)
        console.print("Cliente eliminado exitosamente.",style="bold green")
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
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Opción", style="dim", width=12)
            table.add_column("Descripción")
            table.add_row("1", "Crear Transaccion")
            table.add_row("2", "Listar Transacciones")
            table.add_row("3", "Volver al Menu Principal")
            console.print(table)

            choice = input("Seleccione una opcion: ")
            if choice == '1':
                self.crearTransaccion()
            elif choice == '2':
                self.listarTransacciones()
            elif choice == '3':
                return
            else:
                console.print("Opcion invalida, por favor intente nuevamente.",style="bold red")
    
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
            console.print("Transacción creada exitosamente.",style="bold green")
        except ValueError as e:
            console.print(f"Error en la entrada de datos: {e}", style="bold red")
    
    def listarTransacciones(self):
        console = Console()
        self.limpiar_consola()

        transacciones = self.transaccionesDb.obtenerTodosLosRegistros()  # Obtener todos los registros de la base de datos
        if transacciones:
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("ID-T", style="dim", width=10)
            table.add_column("ID-V", style="dim", width=10)
            table.add_column("ID-C", style="dim", width=10)
            table.add_column("Transacción", style="dim", width=15)
            table.add_column("Fecha", style="dim", width=12)
            table.add_column("Monto", style="dim", width=12, justify="right")
            table.add_column("Observaciones", style="dim", width=20)

            for transaccion in transacciones:
                table.add_row(
                    str(transaccion.get('id_transaccion', 'N/A')),
                    str(transaccion.get('id_vehiculo', 'N/A')),
                    str(transaccion.get('id_cliente', 'N/A')),
                    transaccion.get('tipo_transaccion', 'N/A'),
                    transaccion.get('fecha', 'N/A'),
                    f"${transaccion.get('monto', 'N/A')}",
                    transaccion.get('observaciones', 'N/A')
                )

            console.print(table)
        else:
            console.print("No hay transacciones registradas.", style="bold red")
    #Fin de funciones para transacciones


    #################################
    #FUNCIONES PARA BUSQUEDA AVANZADA
    #################################
    def mostrarVehiculos(self, vehiculos):
        if not vehiculos:
            console.print("No se encontraron vehículos.",style="bold red")
            return
    
    def busquedaAvanzada(self):
        while True:
            try: 
                
                table = Table(show_header=True, header_style="bold blue")
                table.add_column("Opción", style="dim", width=12)
                table.add_column("Descripción")
                table.add_row("1", "Buscar por marca")
                table.add_row("2", "Buscar por estado (Disponible, Reservado, Vendido)")
                table.add_row("3", "Buscar por rango de precio")
                table.add_row("4", " Buscar por rango de precio y estado")
                table.add_row("5", "Volver al menu principal")
                console.print(table)

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
                    if precioMinimo is None:
                        return  # Volver al menu anterior
                    precioMaximo = self.VerificacionDeEntrada("Ingrese el precio maximo (deje en blanco para volver): ", None, lambda x: x == "" or x.isdigit(), "Precio máximo inválido.")
                    if precioMaximo is None:
                        return  # Volver al menu anterior

                    # Convertir a int solo si no es cadena vacía (es decir, si el usuario ingresó un valor numérico)
                    if precioMinimo.strip():  # strip() para asegurarse de no convertir una cadena completamente vacía
                        precioMinimo = int(precioMinimo)
                    else:
                        precioMinimo = None  # Convertir a None si está vacío

                    if precioMaximo.strip():
                        precioMaximo = int(precioMaximo)
                    else:
                        precioMaximo = None  # Convertir a None si está vacío

                    resultados = self.vehiculosDb.buscarPorRangoDePrecio(precioMinimo, precioMaximo)
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
                console.print(f"Error en la entrada de datos: {e}", style="bold red")


if __name__ == "__main__":
    interface = InterfazConcesionario()
    interface.mainMenu()