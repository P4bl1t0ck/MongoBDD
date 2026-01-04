from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from bson.objectid import ObjectId
from typing import List, Dict, Optional, Any
import test

if __name__ == "__main__":
    # Configurar la conexión
    connection_string = "mongodb+srv://AdminUdla:UDLA@clusterpablutus.hneadkh.mongodb.net/?appName=ClusterPablutus"
    db = ConexionMongoDB(connection_string)
    
    # Listar colecciones
    print("\n📋 Colecciones disponibles:")
    colecciones = db.listar_colecciones()
    for col in colecciones:
        print(f"  - {col}")
    
    # Ejemplo: Insertar un usuario
    print("\n➕ Insertando usuario...")
    nuevo_usuario = {
        "nombre": "Juan Pérez",
        "email": "juan@example.com",
        "edad": 25,
        "activo": True
    }
    id_insertado = db.insertar_uno("Usuarios", nuevo_usuario)
    
    # Ejemplo: Obtener todos los usuarios
    print("\n📖 Obteniendo usuarios...")
    usuarios = db.obtener_muchos("Usuarios", limite=5)
    for usuario in usuarios:
        print(f"  - {usuario}")
    
    # Ejemplo: Actualizar un usuario
    if id_insertado:
        print("\n✏️ Actualizando usuario...")
        db.actualizar_uno("Usuarios", {"_id": ObjectId(id_insertado)}, {"edad": 26})
    
    # Ejemplo: Contar documentos
    print("\n🔢 Total de usuarios:")
    total = db.contar_documentos("Usuarios")
    print(f"  Total: {total}")
    
    # Cerrar conexión
    db.desconectar()
