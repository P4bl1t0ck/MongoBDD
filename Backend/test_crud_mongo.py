import os
import sys
from pathlib import Path
from bson.objectid import ObjectId

# Agregar ruta del proyecto al path
sys.path.insert(0, str(Path(__file__).parent))

from conection import ConexionMongoDB

def main():
    # 1️⃣ Obtener URI desde variable de entorno
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("❌ MONGO_URI no está configurada")

    # 2️⃣ Crear conexión
    db = ConexionMongoDB(mongo_uri, "CatequesisDB")

    coleccion = "Usuarios"

    # 3️⃣ INSERT
    print("\n➕ INSERTAR USUARIO")
    usuario = {
        "nombre": "Maria Lopez",
        "email": "maria@example.com",
        "edad": 22,
        "activo": True
    }
    user_id = db.insertar_uno(coleccion, usuario)

    # 4️⃣ READ ALL
    print("\n📖 OBTENER USUARIOS")
    usuarios = db.obtener_muchos(coleccion, limite=5)
    for u in usuarios:
        print(u)

    # 5️⃣ READ BY ID
    if user_id:
        print("\n🔍 OBTENER USUARIO POR ID")
        usuario = db.obtener_por_id(coleccion, user_id)
        print(usuario)

    # 6️⃣ UPDATE
    if user_id:
        print("\n✏️ Actualizar USUARIO")
        db.actualizar_uno(
            coleccion,
            {"_id": ObjectId(user_id)},
            {"edad": 23}
        )

    # 7️⃣ COUNT
    print("\n🔢 CONTAR USUARIOS")
    total = db.contar_documentos(coleccion)
    print(f"Total: {total}")

    # 8️⃣ DELETE
    if user_id:
        print("\n🗑️ ELIMINAR USUARIO")
        db.eliminar_uno(coleccion, {"_id": ObjectId(user_id)})

    # 9️⃣ Cerrar conexión
    db.desconectar()

if __name__ == "__main__":
    main()
