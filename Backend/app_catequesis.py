"""
Backend Flask completo para CatequesisDB
Maneja operaciones CRUD para todas las colecciones:
- Parroquias
- Catequistas
- Grupos
- Catequizandos
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from bson.objectid import ObjectId
from datetime import datetime
from pathlib import Path
from conection import ConexionMongoDB
from schemas import SchemasCatequesis

# ==================== INICIALIZACIÓN ====================

app = Flask(__name__, static_folder='../Frontend', static_url_path='')
CORS(app)  # Permitir peticiones desde el frontend

# Configurar conexión a MongoDB
MONGO_URI = "mongodb+srv://AdminUdla:UDLA@clusterpablutus.hneadkh.mongodb.net/"
db = ConexionMongoDB(MONGO_URI, "CatequesisDB")
schemas = SchemasCatequesis()

# Nombres de colecciones
COL_PARROQUIAS = "parroquias"
COL_CATEQUISTAS = "catequistas"
COL_GRUPOS = "grupos"
COL_CATEQUIZANDOS = "catequizandos"


# ==================== UTILIDADES ====================

def convertir_objectid(documento):
    """Convierte ObjectId a string para JSON"""
    if documento:
        if isinstance(documento, list):
            for doc in documento:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            return documento
        else:
            if '_id' in documento:
                documento['_id'] = str(documento['_id'])
            return documento
    return documento


# ==================== RUTA PRINCIPAL ====================

@app.route('/')
def index():
    """Servir el frontend"""
    return send_from_directory(app.static_folder, 'index.html')


# ==================== PARROQUIAS ====================

@app.route('/api/parroquias', methods=['GET'])
def obtener_parroquias():
    """GET /api/parroquias - Obtiene todas las parroquias"""
    try:
        parroquias = db.obtener_muchos(COL_PARROQUIAS)
        return jsonify({
            "success": True,
            "data": convertir_objectid(parroquias),
            "total": len(parroquias)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/parroquias/<id>', methods=['GET'])
def obtener_parroquia(id):
    """GET /api/parroquias/<id> - Obtiene una parroquia por ID"""
    try:
        parroquia = db.obtener_por_id(COL_PARROQUIAS, id)
        if not parroquia:
            return jsonify({"success": False, "error": "Parroquia no encontrada"}), 404
        return jsonify({
            "success": True,
            "data": convertir_objectid(parroquia)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/parroquias', methods=['POST'])
def crear_parroquia():
    """POST /api/parroquias - Crea una nueva parroquia"""
    try:
        datos = request.get_json()
        
        # Crear documento usando el schema
        parroquia = schemas.parroquia_schema(
            nombre=datos['nombre'],
            nombre_vicaria=datos['nombre_vicaria'],
            ubicacion=datos.get('ubicacion', {"direccion": "", "ciudad": "", "provincia": ""}),
            telefono=datos['telefono'],
            parroco=datos.get('parroco', ''),
            correo=datos.get('correo', ''),
            horarios_misa=datos.get('horarios_misa', []),
            capacidad_catequesis=datos.get('capacidad_catequesis', 0)
        )
        
        parroquia_id = db.insertar_uno(COL_PARROQUIAS, parroquia)
        return jsonify({
            "success": True,
            "message": "Parroquia creada exitosamente",
            "id": parroquia_id
        }), 201
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido faltante: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/parroquias/<id>', methods=['PUT'])
def actualizar_parroquia(id):
    """PUT /api/parroquias/<id> - Actualiza una parroquia"""
    try:
        datos = request.get_json()
        datos['fecha_actualizacion'] = datetime.now()
        
        resultado = db.actualizar_uno(COL_PARROQUIAS, {"_id": ObjectId(id)}, datos)
        if resultado:
            return jsonify({"success": True, "message": "Parroquia actualizada"}), 200
        return jsonify({"success": False, "error": "No se pudo actualizar"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/parroquias/<id>', methods=['DELETE'])
def eliminar_parroquia(id):
    """DELETE /api/parroquias/<id> - Elimina una parroquia"""
    try:
        resultado = db.eliminar_uno(COL_PARROQUIAS, {"_id": ObjectId(id)})
        if resultado:
            return jsonify({"success": True, "message": "Parroquia eliminada"}), 200
        return jsonify({"success": False, "error": "Parroquia no encontrada"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== CATEQUISTAS ====================

@app.route('/api/catequistas', methods=['GET'])
def obtener_catequistas():
    """GET /api/catequistas - Obtiene todos los catequistas"""
    try:
        parroquia_id = request.args.get('parroquia_id')
        filtro = {"parroquia_id": parroquia_id} if parroquia_id else {}
        
        catequistas = db.obtener_muchos(COL_CATEQUISTAS, filtro)
        return jsonify({
            "success": True,
            "data": convertir_objectid(catequistas),
            "total": len(catequistas)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/catequistas/<id>', methods=['GET'])
def obtener_catequista(id):
    """GET /api/catequistas/<id> - Obtiene un catequista por ID"""
    try:
        catequista = db.obtener_por_id(COL_CATEQUISTAS, id)
        if not catequista:
            return jsonify({"success": False, "error": "Catequista no encontrado"}), 404
        return jsonify({
            "success": True,
            "data": convertir_objectid(catequista)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/catequistas', methods=['POST'])
def crear_catequista():
    """POST /api/catequistas - Crea un nuevo catequista"""
    try:
        datos = request.get_json()
        
        catequista = schemas.catequista_schema(
            nombre=datos['nombre'],
            apellido=datos['apellido'],
            correo=datos['correo'],
            edad=int(datos['edad']),
            telefono=datos['telefono'],
            parroquia_id=datos['parroquia_id'],
            cedula=datos.get('cedula', ''),
            direccion=datos.get('direccion', ''),
            especialidad=datos.get('especialidad', ''),
            disponibilidad=datos.get('disponibilidad', [])
        )
        
        catequista_id = db.insertar_uno(COL_CATEQUISTAS, catequista)
        return jsonify({
            "success": True,
            "message": "Catequista creado exitosamente",
            "id": catequista_id
        }), 201
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/catequistas/<id>', methods=['PUT'])
def actualizar_catequista(id):
    """PUT /api/catequistas/<id> - Actualiza un catequista"""
    try:
        datos = request.get_json()
        datos['fecha_actualizacion'] = datetime.now()
        
        resultado = db.actualizar_uno(COL_CATEQUISTAS, {"_id": ObjectId(id)}, datos)
        if resultado:
            return jsonify({"success": True, "message": "Catequista actualizado"}), 200
        return jsonify({"success": False, "error": "No se pudo actualizar"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/catequistas/<id>', methods=['DELETE'])
def eliminar_catequista(id):
    """DELETE /api/catequistas/<id> - Elimina un catequista"""
    try:
        resultado = db.eliminar_uno(COL_CATEQUISTAS, {"_id": ObjectId(id)})
        if resultado:
            return jsonify({"success": True, "message": "Catequista eliminado"}), 200
        return jsonify({"success": False, "error": "Catequista no encontrado"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== GRUPOS ====================

@app.route('/api/grupos', methods=['GET'])
def obtener_grupos():
    """GET /api/grupos - Obtiene todos los grupos"""
    try:
        parroquia_id = request.args.get('parroquia_id')
        filtro = {"parroquia_id": parroquia_id} if parroquia_id else {}
        
        grupos = db.obtener_muchos(COL_GRUPOS, filtro)
        return jsonify({
            "success": True,
            "data": convertir_objectid(grupos),
            "total": len(grupos)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/grupos/<id>', methods=['GET'])
def obtener_grupo(id):
    """GET /api/grupos/<id> - Obtiene un grupo por ID"""
    try:
        grupo = db.obtener_por_id(COL_GRUPOS, id)
        if not grupo:
            return jsonify({"success": False, "error": "Grupo no encontrado"}), 404
        return jsonify({
            "success": True,
            "data": convertir_objectid(grupo)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/grupos', methods=['POST'])
def crear_grupo():
    """POST /api/grupos - Crea un nuevo grupo"""
    try:
        datos = request.get_json()
        
        grupo = schemas.grupo_schema(
            numero_grupo=int(datos['numero_grupo']),
            parroquia_id=datos['parroquia_id'],
            catequista_id=datos['catequista_id'],
            sacramento=datos['sacramento'],
            nivel=datos.get('nivel', ''),
            horario=datos.get('horario', ''),
            aula=datos.get('aula', ''),
            año_lectivo=datos.get('año_lectivo', ''),
            cupo_maximo=int(datos.get('cupo_maximo', 30))
        )
        
        grupo_id = db.insertar_uno(COL_GRUPOS, grupo)
        return jsonify({
            "success": True,
            "message": "Grupo creado exitosamente",
            "id": grupo_id
        }), 201
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/grupos/<id>', methods=['PUT'])
def actualizar_grupo(id):
    """PUT /api/grupos/<id> - Actualiza un grupo"""
    try:
        datos = request.get_json()
        datos['fecha_actualizacion'] = datetime.now()
        
        # Recalcular cupos disponibles si se actualiza el número de estudiantes
        if 'numero_estudiantes' in datos:
            grupo = db.obtener_por_id(COL_GRUPOS, id)
            if grupo:
                datos['cupos_disponibles'] = grupo.get('cupo_maximo', 30) - int(datos['numero_estudiantes'])
        
        resultado = db.actualizar_uno(COL_GRUPOS, {"_id": ObjectId(id)}, datos)
        if resultado:
            return jsonify({"success": True, "message": "Grupo actualizado"}), 200
        return jsonify({"success": False, "error": "No se pudo actualizar"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/grupos/<id>', methods=['DELETE'])
def eliminar_grupo(id):
    """DELETE /api/grupos/<id> - Elimina un grupo"""
    try:
        resultado = db.eliminar_uno(COL_GRUPOS, {"_id": ObjectId(id)})
        if resultado:
            return jsonify({"success": True, "message": "Grupo eliminado"}), 200
        return jsonify({"success": False, "error": "Grupo no encontrado"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== CATEQUIZANDOS ====================

@app.route('/api/catequizandos', methods=['GET'])
def obtener_catequizandos():
    """GET /api/catequizandos - Obtiene todos los catequizandos"""
    try:
        grupo_id = request.args.get('grupo_id')
        parroquia_id = request.args.get('parroquia_id')
        
        filtro = {}
        if grupo_id:
            filtro['grupo_id'] = grupo_id
        if parroquia_id:
            filtro['parroquia_id'] = parroquia_id
        
        catequizandos = db.obtener_muchos(COL_CATEQUIZANDOS, filtro)
        return jsonify({
            "success": True,
            "data": convertir_objectid(catequizandos),
            "total": len(catequizandos)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/catequizandos/<id>', methods=['GET'])
def obtener_catequizando(id):
    """GET /api/catequizandos/<id> - Obtiene un catequizando por ID"""
    try:
        catequizando = db.obtener_por_id(COL_CATEQUIZANDOS, id)
        if not catequizando:
            return jsonify({"success": False, "error": "Catequizando no encontrado"}), 404
        return jsonify({
            "success": True,
            "data": convertir_objectid(catequizando)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/catequizandos', methods=['POST'])
def crear_catequizando():
    """POST /api/catequizandos - Crea un nuevo catequizando"""
    try:
        datos = request.get_json()
        
        # Convertir fecha de nacimiento
        fecha_nac = datetime.strptime(datos['fecha_nacimiento'], '%Y-%m-%d')
        
        catequizando = schemas.catequizando_schema(
            nombre=datos['nombre'],
            apellido=datos['apellido'],
            fecha_nacimiento=fecha_nac,
            telefono=datos['telefono'],
            correo=datos['correo'],
            parroquia_id=datos['parroquia_id'],
            grupo_id=datos['grupo_id'],
            nivel=datos['nivel'],
            cedula=datos.get('cedula', ''),
            direccion=datos.get('direccion', ''),
            nombre_padre=datos.get('nombre_padre', ''),
            nombre_madre=datos.get('nombre_madre', ''),
            telefono_padres=datos.get('telefono_padres', ''),
            padrino=datos.get('padrino'),
            madrina=datos.get('madrina'),
            sacramentos_recibidos=datos.get('sacramentos_recibidos', [])
        )
        
        catequizando_id = db.insertar_uno(COL_CATEQUIZANDOS, catequizando)
        
        # Actualizar contador de estudiantes en el grupo
        grupo = db.obtener_por_id(COL_GRUPOS, datos['grupo_id'])
        if grupo:
            nuevo_total = grupo.get('numero_estudiantes', 0) + 1
            db.actualizar_uno(
                COL_GRUPOS,
                {"_id": ObjectId(datos['grupo_id'])},
                {
                    "numero_estudiantes": nuevo_total,
                    "cupos_disponibles": grupo.get('cupo_maximo', 30) - nuevo_total
                }
            )
        
        return jsonify({
            "success": True,
            "message": "Catequizando inscrito exitosamente",
            "id": catequizando_id
        }), 201
    except KeyError as e:
        return jsonify({"success": False, "error": f"Campo requerido: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/catequizandos/<id>', methods=['PUT'])
def actualizar_catequizando(id):
    """PUT /api/catequizandos/<id> - Actualiza un catequizando"""
    try:
        datos = request.get_json()
        datos['fecha_actualizacion'] = datetime.now()
        
        # Actualizar edad si se cambia fecha de nacimiento
        if 'fecha_nacimiento' in datos:
            if isinstance(datos['fecha_nacimiento'], str):
                fecha_nac = datetime.strptime(datos['fecha_nacimiento'], '%Y-%m-%d')
                datos['fecha_nacimiento'] = fecha_nac
                datos['edad'] = datetime.now().year - fecha_nac.year
        
        resultado = db.actualizar_uno(COL_CATEQUIZANDOS, {"_id": ObjectId(id)}, datos)
        if resultado:
            return jsonify({"success": True, "message": "Catequizando actualizado"}), 200
        return jsonify({"success": False, "error": "No se pudo actualizar"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/catequizandos/<id>', methods=['DELETE'])
def eliminar_catequizando(id):
    """DELETE /api/catequizandos/<id> - Elimina un catequizando"""
    try:
        # Obtener catequizando para actualizar el grupo
        catequizando = db.obtener_por_id(COL_CATEQUIZANDOS, id)
        
        resultado = db.eliminar_uno(COL_CATEQUIZANDOS, {"_id": ObjectId(id)})
        if resultado:
            # Actualizar contador del grupo
            if catequizando and 'grupo_id' in catequizando:
                grupo = db.obtener_por_id(COL_GRUPOS, catequizando['grupo_id'])
                if grupo:
                    nuevo_total = max(0, grupo.get('numero_estudiantes', 0) - 1)
                    db.actualizar_uno(
                        COL_GRUPOS,
                        {"_id": ObjectId(catequizando['grupo_id'])},
                        {
                            "numero_estudiantes": nuevo_total,
                            "cupos_disponibles": grupo.get('cupo_maximo', 30) - nuevo_total
                        }
                    )
            
            return jsonify({"success": True, "message": "Catequizando eliminado"}), 200
        return jsonify({"success": False, "error": "Catequizando no encontrado"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== CONSULTAS Y REPORTES ====================

@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """GET /api/estadisticas - Obtiene estadísticas generales"""
    try:
        stats = {
            "total_parroquias": db.contar_documentos(COL_PARROQUIAS),
            "total_catequistas": db.contar_documentos(COL_CATEQUISTAS),
            "total_grupos": db.contar_documentos(COL_GRUPOS),
            "total_catequizandos": db.contar_documentos(COL_CATEQUIZANDOS),
            "catequistas_activos": db.contar_documentos(COL_CATEQUISTAS, {"activo": True}),
            "grupos_activos": db.contar_documentos(COL_GRUPOS, {"activo": True}),
            "catequizandos_activos": db.contar_documentos(COL_CATEQUIZANDOS, {"activo": True})
        }
        return jsonify({"success": True, "data": stats}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/reportes/por-sacramento', methods=['GET'])
def reporte_por_sacramento():
    """GET /api/reportes/por-sacramento - Catequizandos agrupados por sacramento"""
    try:
        grupos = db.obtener_muchos(COL_GRUPOS)
        
        reporte = {}
        for grupo in grupos:
            sacramento = grupo.get('sacramento', 'Sin especificar')
            if sacramento not in reporte:
                reporte[sacramento] = {
                    "grupos": 0,
                    "estudiantes": 0,
                    "detalles": []
                }
            
            reporte[sacramento]["grupos"] += 1
            reporte[sacramento]["estudiantes"] += grupo.get('numero_estudiantes', 0)
            reporte[sacramento]["detalles"].append({
                "grupo": grupo.get('numero_grupo'),
                "estudiantes": grupo.get('numero_estudiantes', 0),
                "catequista_id": grupo.get('catequista_id')
            })
        
        return jsonify({"success": True, "data": reporte}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """GET /api/health - Verifica el estado del servidor"""
    return jsonify({
        "success": True,
        "message": "Backend CatequesisDB funcionando correctamente",
        "database": "CatequesisDB"
    }), 200


# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({"success": False, "error": "Ruta no encontrada"}), 404


@app.errorhandler(500)
def error_servidor(error):
    return jsonify({"success": False, "error": "Error interno del servidor"}), 500


# ==================== EJECUTAR ====================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 SERVIDOR FLASK - CATEQUESISDB")
    print("="*70)
    print("📝 API disponible en: http://localhost:5001")
    print("🌐 Frontend disponible en: http://localhost:5001")
    print("\n📚 RUTAS API:")
    print("\n  PARROQUIAS:")
    print("    GET    /api/parroquias")
    print("    POST   /api/parroquias")
    print("    GET    /api/parroquias/<id>")
    print("    PUT    /api/parroquias/<id>")
    print("    DELETE /api/parroquias/<id>")
    print("\n  CATEQUISTAS:")
    print("    GET    /api/catequistas?parroquia_id=<id>")
    print("    POST   /api/catequistas")
    print("    GET    /api/catequistas/<id>")
    print("    PUT    /api/catequistas/<id>")
    print("    DELETE /api/catequistas/<id>")
    print("\n  GRUPOS:")
    print("    GET    /api/grupos?parroquia_id=<id>")
    print("    POST   /api/grupos")
    print("    GET    /api/grupos/<id>")
    print("    PUT    /api/grupos/<id>")
    print("    DELETE /api/grupos/<id>")
    print("\n  CATEQUIZANDOS:")
    print("    GET    /api/catequizandos?grupo_id=<id>&parroquia_id=<id>")
    print("    POST   /api/catequizandos")
    print("    GET    /api/catequizandos/<id>")
    print("    PUT    /api/catequizandos/<id>")
    print("    DELETE /api/catequizandos/<id>")
    print("\n  REPORTES:")
    print("    GET    /api/estadisticas")
    print("    GET    /api/reportes/por-sacramento")
    print("    GET    /api/health")
    print("\n" + "="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
