import pymongo as pm
from pymongo.errors import ServerSelectionTimeoutError
from bson.objectid import ObjectId
from typing import List, Dict, Optional

class ConexionMongoDB:
    """
    Clase para manejar todas las operaciones CRUD con MongoDB.
    """
    
    def __init__(self, connection_string: str, database_name: str = "CatequesisDB"):
        """
        Inicializa la conexión a MongoDB.
        
        Args:
            connection_string: URL de conexión a MongoDB Atlas
            database_name: Nombre de la base de datos (por defecto: CatequesisDB)
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.db = None
        self.conectar()
    
    def conectar(self) -> bool:
        """
        Establece la conexión a MongoDB.
        
        Returns:
            True si la conexión es exitosa, False en caso contrario.
        """
        try:
            self.client = pm.MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]
            print(f" Conexión exitosa a MongoDB - Base de datos: {self.database_name}")
            return True
        except ServerSelectionTimeoutError:
            print(" Error: No se pudo conectar al servidor MongoDB")
            return False
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False
    
    def desconectar(self) -> None:
        """Cierra la conexión con MongoDB."""
        if self.client:
            self.client.close()
            print(" Desconexión completada")
    
    def listar_colecciones(self) -> List[str]:
        """
        Lista todas las colecciones disponibles.
        
        Returns:
            Lista de nombres de colecciones.
        """
        try:
            return self.db.list_collection_names()
        except Exception as e:
            print(f"Error al listar colecciones: {e}")
            return []
    
    # ==================== OPERACIONES CRUD ====================
    
    def insertar_uno(self, coleccion: str, documento: Dict) -> Optional[str]:
        """
        Inserta un documento en la colección.
        
        Args:
            coleccion: Nombre de la colección
            documento: Diccionario con los datos a insertar
            
        Returns:
            ID del documento insertado, None si hay error.
        """
        try:
            resultado = self.db[coleccion].insert_one(documento)
            print(f" Documento insertado con ID: {resultado.inserted_id}")
            return str(resultado.inserted_id)
        except Exception as e:
            print(f" Error al insertar documento: {e}")
            return None
    
    def insertar_muchos(self, coleccion: str, documentos: List[Dict]) -> Optional[List[str]]:
        
        #Inserta múltiples documentos.
       
        try:
            resultado = self.db[coleccion].insert_many(documentos)
            ids = [str(id) for id in resultado.inserted_ids]
            print(f"{len(ids)} documentos insertados")
            return ids
        except Exception as e:
            print(f" Error al insertar documentos: {e}")
            return None
    
    
    
    def obtener_uno(self, coleccion: str, filtro: Dict) -> Optional[Dict]:
        #Obtiene un documento que cumple el filtro.
        try:
            return self.db[coleccion].find_one(filtro)
        except Exception as e:
            print(f" Error al buscar documento: {e}")
            return None
    
    def obtener_muchos(self, coleccion: str, filtro: Dict = None, limite: int = 0) -> List[Dict]:
        #Obtiene múltiples documentos.
    
        try:
            if filtro is None:
                filtro = {}
            query = self.db[coleccion].find(filtro)
            if limite > 0:
                query = query.limit(limite)
            return list(query)
        except Exception as e:
            print(f" Error al buscar documentos: {e}")
            return []
    
    def obtener_por_id(self, coleccion: str, doc_id: str) -> Optional[Dict]:
        #Obtiene un documento por su ID.
        try:
            return self.db[coleccion].find_one({"_id": ObjectId(doc_id)})
        except Exception as e:
            print(f" Error al obtener documento por ID: {e}")
            return None
    
    def contar_documentos(self, coleccion: str, filtro: Dict = None) -> int:        
        #Cuenta documentos que cumplen el filtro.
        try:
            if filtro is None:
                filtro = {}
            return self.db[coleccion].count_documents(filtro)
        except Exception as e:
            print(f" Error al contar documentos: {e}")
            return 0
    
    
    
    def actualizar_uno(self, coleccion: str, filtro: Dict, nuevos_datos: Dict) -> bool:
       #Actualiza un documento.
        try:
            resultado = self.db[coleccion].update_one(filtro, {"$set": nuevos_datos})
            if resultado.modified_count > 0:
                print(" Documento actualizado")
                return True
            else:
                print("⚠ No se encontró documento para actualizar")
                return False
        except Exception as e:
            print(f" Error al actualizar documento: {e}")
            return False
    
    def actualizar_muchos(self, coleccion: str, filtro: Dict, nuevos_datos: Dict) -> int:
        """
        Actualiza múltiples documentos.
        
        Args:
            coleccion: Nombre de la colección
            filtro: Criterios de búsqueda
            nuevos_datos: Datos a actualizar
            
        Returns:
            Número de documentos actualizados.
        """
        try:
            resultado = self.db[coleccion].update_many(filtro, {"$set": nuevos_datos})
            print(f" {resultado.modified_count} documentos actualizados")
            return resultado.modified_count
        except Exception as e:
            print(f" Error al actualizar documentos: {e}")
            return 0
    
    
    def eliminar_uno(self, coleccion: str, filtro: Dict) -> bool:    
        #Elimina un documento.
    
        try:
            resultado = self.db[coleccion].delete_one(filtro)
            if resultado.deleted_count > 0:
                print(" Documento eliminado")
                return True
            else:
                print("⚠ No se encontró documento para eliminar")
                return False
        except Exception as e:
            print(f" Error al eliminar documento: {e}")
            return False
    
    def eliminar_muchos(self, coleccion: str, filtro: Dict) -> int:
        #Elimina múltiples documentos.
        try:
            resultado = self.db[coleccion].delete_many(filtro)
            print(f"{resultado.deleted_count} documentos eliminados")
            return resultado.deleted_count
        except Exception as e:
            print(f" Error al eliminar documentos: {e}")
            return 0

