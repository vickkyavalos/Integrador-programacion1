import json
import os

class Database:
    def __init__(self, rutaDeArchivo):
        self.rutaDeArchivo = rutaDeArchivo
        self.data = self.cargarData()

    def cargarData(self):
        if os.path.exists(self.rutaDeArchivo):
            try:
                with open(self.rutaDeArchivo, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []  # Archivo está vacío o no es un JSON válido
        else:
            return []

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