"""
Backend Flask simple para CatequesisDB
Maneja operaciones CRUD para usuarios
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from bson.objectid import ObjectId
import os
import sys
from pathlib import Path

# Agregar ruta del proyecto al path
sys.path.insert(0, str(Path(__file__).parent.parent / "MongoDBProyect"))

from conection import ConexionMongoDB

# ==================== INICIALIZACIÓN ====================

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde el frontend

# Configurar conexión a MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://AdminUdla:UDLA@clusterpablutus.hneadkh.mongodb.net/?appName=ClusterPablutus")
db = ConexionMongoDB(MONGO_URI, "CatequesisDB")

COLECCION = "Usuarios"


# ==================== RUTAS CRUD ====================

@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    """
    GET /api/usuarios - Obtiene todos los usuarios
    Parámetros opcionales:
    - limite: número máximo de resultados (default: 10)
    """
    try:
        limite = request.args.get('limite', 10, type=int)
        usuarios = db.obtener_muchos(COLECCION, limite=limite)
        
        # Convertir ObjectId a string para JSON
        usuarios_json = []
        for u in usuarios:
            u['_id'] = str(u['_id'])
            usuarios_json.append(u)
        
        return jsonify({
            "success": True,
            "data": usuarios_json,
            "total": len(usuarios_json)
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/usuarios/<id>', methods=['GET'])
def obtener_usuario(id):
    """
    GET /api/usuarios/<id> - Obtiene un usuario por ID
    """
    try:
        usuario = db.obtener_por_id(COLECCION, id)
        
        if not usuario:
            return jsonify({
                "success": False,
                "error": "Usuario no encontrado"
            }), 404
        
        usuario['_id'] = str(usuario['_id'])
        return jsonify({
            "success": True,
            "data": usuario
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    """
    POST /api/usuarios - Crea un nuevo usuario
    Body esperado:
    {
        "nombre": "Juan",
        "email": "juan@mail.com",
        "edad": 25
    }
    """
    try:
        datos = request.get_json()
        
        # Validar que tenga los campos necesarios
        if not datos or 'nombre' not in datos or 'email' not in datos:
            return jsonify({
                "success": False,
                "error": "Se requieren 'nombre' y 'email'"
            }), 400
        
        # Crear documento
        nuevo_usuario = {
            "nombre": datos['nombre'],
            "email": datos['email'],
            "edad": datos.get('edad', None),
            "activo": True
        }
        
        user_id = db.insertar_uno(COLECCION, nuevo_usuario)
        
        return jsonify({
            "success": True,
            "message": "Usuario creado exitosamente",
            "id": user_id
        }), 201
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/usuarios/<id>', methods=['PUT'])
def actualizar_usuario(id):
    """
    PUT /api/usuarios/<id> - Actualiza un usuario
    Body esperado:
    {
        "nombre": "Juan Nuevo",
        "email": "nuevo@mail.com",
        "edad": 26
    }
    """
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                "success": False,
                "error": "Se requieren datos para actualizar"
            }), 400
        
        resultado = db.actualizar_uno(
            COLECCION,
            {"_id": ObjectId(id)},
            datos
        )
        
        if resultado:
            return jsonify({
                "success": True,
                "message": "Usuario actualizado exitosamente"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "No se pudo actualizar el usuario"
            }), 400
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/usuarios/<id>', methods=['DELETE'])
def eliminar_usuario(id):
    """
    DELETE /api/usuarios/<id> - Elimina un usuario
    """
    try:
        resultado = db.eliminar_uno(COLECCION, {"_id": ObjectId(id)})
        
        if resultado:
            return jsonify({
                "success": True,
                "message": "Usuario eliminado exitosamente"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "No se encontró el usuario"
            }), 404
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==================== RUTAS UTILIDAD ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    GET /api/health - Verifica que el servidor está funcionando
    """
    return jsonify({
        "success": True,
        "message": "Backend funcionando correctamente"
    }), 200


@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """
    GET /api/estadisticas - Obtiene estadísticas de usuarios
    """
    try:
        total = db.contar_documentos(COLECCION)
        return jsonify({
            "success": True,
            "total_usuarios": total
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({
        "success": False,
        "error": "Ruta no encontrada"
    }), 404


@app.errorhandler(500)
def error_servidor(error):
    return jsonify({
        "success": False,
        "error": "Error interno del servidor"
    }), 500


# ==================== EJECUTAR ====================

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("📝 API disponible en http://localhost:5000")
    print("📚 Documentación de rutas:")
    print("   - GET    /api/usuarios              - Obtener todos los usuarios")
    print("   - GET    /api/usuarios/<id>         - Obtener usuario por ID")
    print("   - POST   /api/usuarios              - Crear usuario")
    print("   - PUT    /api/usuarios/<id>         - Actualizar usuario")
    print("   - DELETE /api/usuarios/<id>         - Eliminar usuario")
    print("   - GET    /api/estadisticas          - Obtener estadísticas")
    print("   - GET    /api/health                - Verificar servidor\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
