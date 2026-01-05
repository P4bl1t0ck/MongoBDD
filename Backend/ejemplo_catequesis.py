"""
Ejemplo completo de uso de CatequesisDB con todas las colecciones
Demuestra operaciones CRUD para: parroquias, catequistas, grupos y catequizandos
"""

from conection import ConexionMongoDB
from schemas import SchemasCatequesis
from datetime import datetime
from bson.objectid import ObjectId

def main():
    # ==================== CONFIGURACIÓN ====================
    print("\n" + "="*70)
    print("  SISTEMA DE GESTIÓN DE CATEQUESIS - CatequesisDB")
    print("="*70)
    
    # String de conexión a MongoDB Atlas
    MONGO_URI = "mongodb+srv://AdminUdla:UDLA@clusterpablutus.hneadkh.mongodb.net/"
    
    # Conectar a la base de datos
    db = ConexionMongoDB(MONGO_URI, "CatequesisDB")
    schemas = SchemasCatequesis()
    
    # Nombres de las colecciones
    COL_PARROQUIAS = "parroquias"
    COL_CATEQUISTAS = "catequistas"
    COL_GRUPOS = "grupos"
    COL_CATEQUIZANDOS = "catequizandos"
    
    # ==================== 1. CREAR PARROQUIAS ====================
    print("\n" + "="*70)
    print("1️⃣  CREAR PARROQUIAS")
    print("="*70)
    
    parroquia1 = schemas.parroquia_schema(
        nombre="Parroquia San José",
        nombre_vicaria="Vicaría Norte",
        ubicacion={
            "direccion": "Av. 6 de Diciembre N34-123",
            "ciudad": "Quito",
            "provincia": "Pichincha",
            "coordenadas": {"lat": -0.1865, "lng": -78.4305}
        },
        telefono="02-2456789",
        parroco="Padre Juan Pérez",
        correo="sanjose@catequesis.ec",
        horarios_misa=["Lunes a Viernes 7:00 AM", "Sábado 6:00 PM", "Domingo 9:00 AM y 11:00 AM"],
        capacidad_catequesis=200
    )
    
    parroquia2 = schemas.parroquia_schema(
        nombre="Parroquia María Auxiliadora",
        nombre_vicaria="Vicaría Sur",
        ubicacion={
            "direccion": "Av. Maldonado S25-456",
            "ciudad": "Quito",
            "provincia": "Pichincha",
            "coordenadas": {"lat": -0.2890, "lng": -78.5401}
        },
        telefono="02-3456789",
        parroco="Padre Carlos González",
        correo="mariaauxiliadora@catequesis.ec",
        capacidad_catequesis=150
    )
    
    parroquia1_id = db.insertar_uno(COL_PARROQUIAS, parroquia1)
    parroquia2_id = db.insertar_uno(COL_PARROQUIAS, parroquia2)
    
    print(f"\n✅ Parroquias creadas:")
    print(f"  • {parroquia1['nombre']} - ID: {parroquia1_id}")
    print(f"  • {parroquia2['nombre']} - ID: {parroquia2_id}")
    
    # ==================== 2. CREAR CATEQUISTAS ====================
    print("\n" + "="*70)
    print("2️⃣  CREAR CATEQUISTAS")
    print("="*70)
    
    catequista1 = schemas.catequista_schema(
        nombre="María",
        apellido="González",
        correo="maria.gonzalez@email.com",
        edad=35,
        telefono="0998765432",
        parroquia_id=parroquia1_id,
        cedula="1712345678",
        direccion="Calle A 123, Quito",
        especialidad="Primera Comunión",
        disponibilidad=["Sábados 9:00 AM - 12:00 PM", "Domingos 3:00 PM - 5:00 PM"]
    )
    
    catequista2 = schemas.catequista_schema(
        nombre="Carlos",
        apellido="López",
        correo="carlos.lopez@email.com",
        edad=42,
        telefono="0987654321",
        parroquia_id=parroquia1_id,
        cedula="1723456789",
        direccion="Av. B 456, Quito",
        especialidad="Confirmación",
        disponibilidad=["Sábados 2:00 PM - 5:00 PM"]
    )
    
    catequista3 = schemas.catequista_schema(
        nombre="Ana",
        apellido="Martínez",
        correo="ana.martinez@email.com",
        edad=28,
        telefono="0976543210",
        parroquia_id=parroquia2_id,
        cedula="1734567890",
        especialidad="Primera Comunión"
    )
    
    catequista1_id = db.insertar_uno(COL_CATEQUISTAS, catequista1)
    catequista2_id = db.insertar_uno(COL_CATEQUISTAS, catequista2)
    catequista3_id = db.insertar_uno(COL_CATEQUISTAS, catequista3)
    
    print(f"\n✅ Catequistas creados:")
    print(f"  • {catequista1['nombre_completo']} - {catequista1['especialidad']}")
    print(f"  • {catequista2['nombre_completo']} - {catequista2['especialidad']}")
    print(f"  • {catequista3['nombre_completo']} - {catequista3['especialidad']}")
    
    # ==================== 3. CREAR GRUPOS ====================
    print("\n" + "="*70)
    print("3️⃣  CREAR GRUPOS DE CATEQUESIS")
    print("="*70)
    
    grupo1 = schemas.grupo_schema(
        numero_grupo=101,
        parroquia_id=parroquia1_id,
        catequista_id=catequista1_id,
        sacramento="Primera Comunión",
        nivel="Nivel 1",
        horario="Sábados 9:00 AM - 11:00 AM",
        aula="Salón Principal - Piso 2",
        año_lectivo="2025-2026",
        cupo_maximo=25
    )
    
    grupo2 = schemas.grupo_schema(
        numero_grupo=102,
        parroquia_id=parroquia1_id,
        catequista_id=catequista2_id,
        sacramento="Confirmación",
        nivel="Nivel 2",
        horario="Sábados 2:00 PM - 4:00 PM",
        aula="Salón 201",
        año_lectivo="2025-2026",
        cupo_maximo=30
    )
    
    grupo3 = schemas.grupo_schema(
        numero_grupo=201,
        parroquia_id=parroquia2_id,
        catequista_id=catequista3_id,
        sacramento="Primera Comunión",
        nivel="Nivel 1",
        horario="Domingos 10:00 AM - 12:00 PM",
        aula="Aula 1",
        año_lectivo="2025-2026",
        cupo_maximo=20
    )
    
    grupo1_id = db.insertar_uno(COL_GRUPOS, grupo1)
    grupo2_id = db.insertar_uno(COL_GRUPOS, grupo2)
    grupo3_id = db.insertar_uno(COL_GRUPOS, grupo3)
    
    print(f"\n✅ Grupos creados:")
    print(f"  • Grupo {grupo1['numero_grupo']} - {grupo1['sacramento']} - {grupo1['horario']}")
    print(f"  • Grupo {grupo2['numero_grupo']} - {grupo2['sacramento']} - {grupo2['horario']}")
    print(f"  • Grupo {grupo3['numero_grupo']} - {grupo3['sacramento']} - {grupo3['horario']}")
    
    # ==================== 4. CREAR CATEQUIZANDOS ====================
    print("\n" + "="*70)
    print("4️⃣  CREAR CATEQUIZANDOS (ESTUDIANTES)")
    print("="*70)
    
    catequizando1 = schemas.catequizando_schema(
        nombre="Sofía",
        apellido="Ramírez",
        fecha_nacimiento=datetime(2015, 5, 15),
        telefono="0965432109",
        correo="sofia.ramirez@email.com",
        parroquia_id=parroquia1_id,
        grupo_id=grupo1_id,
        nivel="Nivel 1",
        cedula="1745678901",
        direccion="Calle C 789, Quito",
        nombre_padre="Roberto Ramírez",
        nombre_madre="Laura Pérez",
        telefono_padres="0998765432",
        padrino={"nombre": "Jorge Ramírez", "telefono": "0987654321", "parroquia_bautismo": "San Juan"},
        madrina={"nombre": "Patricia López", "telefono": "0976543210", "parroquia_bautismo": "San Juan"},
        certificados=[
            {"tipo": "Bautismo", "fecha": "2015-08-20", "parroquia": "San Juan", "numero": "B-2015-456"}
        ],
        sacramentos_recibidos=["Bautismo"]
    )
    
    catequizando2 = schemas.catequizando_schema(
        nombre="Miguel",
        apellido="Torres",
        fecha_nacimiento=datetime(2014, 9, 22),
        telefono="0954321098",
        correo="miguel.torres@email.com",
        parroquia_id=parroquia1_id,
        grupo_id=grupo1_id,
        nivel="Nivel 1",
        nombre_padre="Luis Torres",
        nombre_madre="Carmen Silva",
        telefono_padres="0987654321",
        padrino={"nombre": "Pedro Torres", "telefono": "0976543210"},
        madrina={"nombre": "Isabel Gómez", "telefono": "0965432109"},
        sacramentos_recibidos=["Bautismo"]
    )
    
    catequizando3 = schemas.catequizando_schema(
        nombre="Valentina",
        apellido="Morales",
        fecha_nacimiento=datetime(2012, 3, 10),
        telefono="0943210987",
        correo="valentina.morales@email.com",
        parroquia_id=parroquia1_id,
        grupo_id=grupo2_id,
        nivel="Nivel 2",
        nombre_padre="Fernando Morales",
        nombre_madre="Andrea Castillo",
        telefono_padres="0976543210",
        sacramentos_recibidos=["Bautismo", "Primera Comunión"]
    )
    
    catequizando1_id = db.insertar_uno(COL_CATEQUIZANDOS, catequizando1)
    catequizando2_id = db.insertar_uno(COL_CATEQUIZANDOS, catequizando2)
    catequizando3_id = db.insertar_uno(COL_CATEQUIZANDOS, catequizando3)
    
    print(f"\n✅ Catequizandos inscritos:")
    print(f"  • {catequizando1['nombre_completo']} - {catequizando1['edad']} años - Grupo {grupo1['numero_grupo']}")
    print(f"  • {catequizando2['nombre_completo']} - {catequizando2['edad']} años - Grupo {grupo1['numero_grupo']}")
    print(f"  • {catequizando3['nombre_completo']} - {catequizando3['edad']} años - Grupo {grupo2['numero_grupo']}")
    
    # ==================== 5. ACTUALIZAR RELACIONES ====================
    print("\n" + "="*70)
    print("5️⃣  ACTUALIZAR RELACIONES ENTRE COLECCIONES")
    print("="*70)
    
    # Actualizar grupo 1 con los catequizandos
    db.actualizar_uno(
        COL_GRUPOS,
        {"_id": ObjectId(grupo1_id)},
        {
            "catequizandos_ids": [catequizando1_id, catequizando2_id],
            "numero_estudiantes": 2,
            "cupos_disponibles": 23
        }
    )
    
    # Actualizar grupo 2 con catequizando
    db.actualizar_uno(
        COL_GRUPOS,
        {"_id": ObjectId(grupo2_id)},
        {
            "catequizandos_ids": [catequizando3_id],
            "numero_estudiantes": 1,
            "cupos_disponibles": 29
        }
    )
    
    # Actualizar catequista 1 con sus grupos
    db.actualizar_uno(
        COL_CATEQUISTAS,
        {"_id": ObjectId(catequista1_id)},
        {"grupos_ids": [grupo1_id]}
    )
    
    # Actualizar catequista 2 con sus grupos
    db.actualizar_uno(
        COL_CATEQUISTAS,
        {"_id": ObjectId(catequista2_id)},
        {"grupos_ids": [grupo2_id]}
    )
    
    print("✅ Relaciones actualizadas correctamente")
    
    # ==================== 6. CONSULTAS Y REPORTES ====================
    print("\n" + "="*70)
    print("6️⃣  CONSULTAS Y REPORTES")
    print("="*70)
    
    # Listar todas las parroquias
    print("\n📍 PARROQUIAS REGISTRADAS:")
    parroquias = db.obtener_muchos(COL_PARROQUIAS)
    for p in parroquias:
        print(f"  • {p['nombre']} - {p['nombre_vicaria']}")
        print(f"    Dirección: {p['ubicacion']['direccion']}, {p['ubicacion']['ciudad']}")
        print(f"    Teléfono: {p['telefono']}")
        print(f"    Capacidad: {p['capacidad_catequesis']} estudiantes")
    
    # Listar catequistas por parroquia
    print(f"\n👥 CATEQUISTAS DE {parroquia1['nombre'].upper()}:")
    catequistas_p1 = db.obtener_muchos(COL_CATEQUISTAS, {"parroquia_id": parroquia1_id})
    for c in catequistas_p1:
        print(f"  • {c['nombre_completo']} - {c['especialidad']}")
        print(f"    Contacto: {c['correo']} | {c['telefono']}")
    
    # Listar grupos con su información
    print("\n📚 GRUPOS DE CATEQUESIS:")
    grupos = db.obtener_muchos(COL_GRUPOS)
    for g in grupos:
        print(f"  • Grupo {g['numero_grupo']} - {g['sacramento']}")
        print(f"    Horario: {g['horario']}")
        print(f"    Estudiantes: {g['numero_estudiantes']}/{g['cupo_maximo']}")
        print(f"    Cupos disponibles: {g['cupos_disponibles']}")
    
    # Listar catequizandos de un grupo específico
    print(f"\n👦 ESTUDIANTES DEL GRUPO {grupo1['numero_grupo']}:")
    estudiantes_g1 = db.obtener_muchos(COL_CATEQUIZANDOS, {"grupo_id": grupo1_id})
    for e in estudiantes_g1:
        print(f"  • {e['nombre_completo']} - {e['edad']} años")
        print(f"    Contacto: {e['telefono_padres']} ({e['nombre_padre']} / {e['nombre_madre']})")
        print(f"    Sacramentos recibidos: {', '.join(e['sacramentos_recibidos'])}")
    
    # Estadísticas generales
    print("\n" + "="*70)
    print("📊 ESTADÍSTICAS GENERALES")
    print("="*70)
    
    total_parroquias = db.contar_documentos(COL_PARROQUIAS)
    total_catequistas = db.contar_documentos(COL_CATEQUISTAS)
    total_grupos = db.contar_documentos(COL_GRUPOS)
    total_catequizandos = db.contar_documentos(COL_CATEQUIZANDOS)
    
    print(f"  📍 Parroquias: {total_parroquias}")
    print(f"  👥 Catequistas: {total_catequistas}")
    print(f"  📚 Grupos: {total_grupos}")
    print(f"  👦 Catequizandos: {total_catequizandos}")
    
    # Buscar catequizandos que necesitan confirmación
    print("\n🔍 CATEQUIZANDOS PREPARÁNDOSE PARA CONFIRMACIÓN:")
    preparando_confirmacion = db.obtener_muchos(
        COL_CATEQUIZANDOS,
        {"grupo_id": grupo2_id}
    )
    for c in preparando_confirmacion:
        print(f"  • {c['nombre_completo']} - {c['edad']} años")
    
    # ==================== 7. EJEMPLO DE ACTUALIZACIÓN ====================
    print("\n" + "="*70)
    print("7️⃣  EJEMPLO DE ACTUALIZACIÓN")
    print("="*70)
    
    # Actualizar información de un catequizando
    print(f"\n✏️  Actualizando información de {catequizando1['nombre_completo']}...")
    db.actualizar_uno(
        COL_CATEQUIZANDOS,
        {"_id": ObjectId(catequizando1_id)},
        {
            "observaciones_medicas": "Alergia al polen",
            "notas": "Estudiante destacada, muy participativa"
        }
    )
    print("✅ Información actualizada")
    
    # Verificar actualización
    catequizando_actualizado = db.obtener_por_id(COL_CATEQUIZANDOS, catequizando1_id)
    print(f"  Observaciones médicas: {catequizando_actualizado['observaciones_medicas']}")
    print(f"  Notas: {catequizando_actualizado['notas']}")
    
    # ==================== 8. EJEMPLO DE ELIMINACIÓN ====================
    print("\n" + "="*70)
    print("8️⃣  INFORMACIÓN SOBRE ELIMINACIÓN")
    print("="*70)
    
    print("\n⚠️  NOTA: Para eliminar documentos, usa:")
    print("  • db.eliminar_uno(coleccion, filtro)")
    print("  • db.eliminar_muchos(coleccion, filtro)")
    print("\n  Ejemplo:")
    print("    # Eliminar catequizando inactivo")
    print("    # db.eliminar_uno(COL_CATEQUIZANDOS, {'_id': ObjectId(id), 'activo': False})")
    print("\n  ⚠️  ¡Siempre verifica antes de eliminar!")
    
    # ==================== FINALIZACIÓN ====================
    print("\n" + "="*70)
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("="*70)
    
    db.desconectar()
    print("\n")


if __name__ == "__main__":
    main()
