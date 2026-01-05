"""
Ejemplo de uso de la clase ConexionMongoDB
Para ejecutar operaciones CRUD con tu base de datos MongoDB Atlas
"""

from conection import ConexionMongoDB
from bson.objectid import ObjectId

def main():
    # ==================== CONFIGURACIÓN ====================
    
    # Tu string de conexión a MongoDB Atlas
    MONGO_URI = "mongodb+srv://AdminUdla:UDLA@clusterpablutus.hneadkh.mongodb.net/"
    
    # Nombre de tu base de datos (CÁMBIALO según tus necesidades)
    DATABASE_NAME = "MiBaseDatos"
    
    # Nombre de tu colección (CÁMBIALO según tus necesidades)
    COLECCION = "Usuarios"
    
    # ==================== CONEXIÓN ====================
    print("\n" + "="*60)
    print("CONECTANDO A MONGODB ATLAS")
    print("="*60)
    
    db = ConexionMongoDB(MONGO_URI, DATABASE_NAME)
    
    # Listar colecciones existentes
    print("\n📁 Colecciones disponibles:")
    colecciones = db.listar_colecciones()
    if colecciones:
        for col in colecciones:
            print(f"  - {col}")
    else:
        print("  (No hay colecciones aún)")
    
    # ==================== CREATE (INSERTAR) ====================
    print("\n" + "="*60)
    print("1️⃣  CREATE - INSERTAR DOCUMENTOS")
    print("="*60)
    
    # Insertar un solo documento
    print("\n➕ Insertando un usuario...")
    nuevo_usuario = {
        "nombre": "Juan Pérez",
        "email": "juan@example.com",
        "edad": 25,
        "ciudad": "Quito",
        "activo": True
    }
    user_id = db.insertar_uno(COLECCION, nuevo_usuario)
    
    # Insertar múltiples documentos
    print("\n➕ Insertando múltiples usuarios...")
    usuarios = [
        {
            "nombre": "María González",
            "email": "maria@example.com",
            "edad": 30,
            "ciudad": "Guayaquil",
            "activo": True
        },
        {
            "nombre": "Carlos López",
            "email": "carlos@example.com",
            "edad": 28,
            "ciudad": "Cuenca",
            "activo": False
        },
        {
            "nombre": "Ana Martínez",
            "email": "ana@example.com",
            "edad": 22,
            "ciudad": "Quito",
            "activo": True
        }
    ]
    ids_insertados = db.insertar_muchos(COLECCION, usuarios)
    
    # ==================== READ (LEER) ====================
    print("\n" + "="*60)
    print("2️⃣  READ - LEER DOCUMENTOS")
    print("="*60)
    
    # Obtener todos los usuarios (con límite)
    print("\n📖 Obteniendo todos los usuarios (límite 10):")
    todos_usuarios = db.obtener_muchos(COLECCION, limite=10)
    for usuario in todos_usuarios:
        print(f"  • {usuario['nombre']} - {usuario['email']} (Edad: {usuario['edad']})")
    
    # Contar documentos
    total = db.contar_documentos(COLECCION)
    print(f"\n📊 Total de usuarios en la base de datos: {total}")
    
    # Obtener usuario por ID
    if user_id:
        print(f"\n🔍 Obteniendo usuario por ID ({user_id}):")
        usuario = db.obtener_por_id(COLECCION, user_id)
        if usuario:
            print(f"  Nombre: {usuario['nombre']}")
            print(f"  Email: {usuario['email']}")
            print(f"  Edad: {usuario['edad']}")
            print(f"  Ciudad: {usuario['ciudad']}")
    
    # Buscar con filtro
    print("\n🔍 Buscando usuarios de Quito:")
    usuarios_quito = db.obtener_muchos(COLECCION, filtro={"ciudad": "Quito"})
    for usuario in usuarios_quito:
        print(f"  • {usuario['nombre']} - {usuario['email']}")
    
    # Buscar un solo usuario con filtro
    print("\n🔍 Buscando un usuario activo:")
    usuario_activo = db.obtener_uno(COLECCION, {"activo": True})
    if usuario_activo:
        print(f"  {usuario_activo['nombre']} - {usuario_activo['email']}")
    
    # ==================== UPDATE (ACTUALIZAR) ====================
    print("\n" + "="*60)
    print("3️⃣  UPDATE - ACTUALIZAR DOCUMENTOS")
    print("="*60)
    
    # Actualizar un documento por ID
    if user_id:
        print(f"\n✏️  Actualizando edad del usuario con ID {user_id}...")
        db.actualizar_uno(
            COLECCION,
            {"_id": ObjectId(user_id)},
            {"edad": 26, "ciudad": "Loja"}
        )
        
        # Verificar actualización
        usuario_actualizado = db.obtener_por_id(COLECCION, user_id)
        if usuario_actualizado:
            print(f"  Nueva edad: {usuario_actualizado['edad']}")
            print(f"  Nueva ciudad: {usuario_actualizado['ciudad']}")
    
    # Actualizar múltiples documentos
    print("\n✏️  Actualizando todos los usuarios de Quito...")
    count = db.actualizar_muchos(
        COLECCION,
        {"ciudad": "Quito"},
        {"ciudad": "Quito - Ecuador"}
    )
    print(f"  {count} documentos actualizados")
    
    # ==================== DELETE (ELIMINAR) ====================
    print("\n" + "="*60)
    print("4️⃣  DELETE - ELIMINAR DOCUMENTOS")
    print("="*60)
    
    # Eliminar un documento
    print("\n🗑️  Eliminando usuarios inactivos...")
    eliminados = db.eliminar_muchos(COLECCION, {"activo": False})
    print(f"  {eliminados} usuarios eliminados")
    
    # Contar documentos restantes
    total_final = db.contar_documentos(COLECCION)
    print(f"\n📊 Total de usuarios después de eliminar: {total_final}")
    
    # ==================== DESCONEXIÓN ====================
    print("\n" + "="*60)
    print("CERRANDO CONEXIÓN")
    print("="*60 + "\n")
    db.desconectar()


if __name__ == "__main__":
    main()
