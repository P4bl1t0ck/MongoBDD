"""
Esquemas y estructuras de datos para CatequesisDB
Define la estructura de cada colección en MongoDB
"""

from datetime import datetime
from typing import List

class SchemasCatequesis:
    """
    Clase que define los esquemas de datos para las colecciones de CatequesisDB.
    MongoDB no requiere esquemas rígidos, pero esto sirve como documentación y validación.
    """
    
    @staticmethod
    def catequista_schema(
        nombre: str,
        apellido: str,
        correo: str,
        edad: int,
        telefono: str,
        parroquia_id: str,  # Referencia a la colección parroquias
        grupos_ids: List[str] = None,  # Lista de IDs de grupos que imparte
        cedula: str = "",
        direccion: str = "",
        fecha_inicio: datetime = None,
        especialidad: str = "",  # ej: "Primera Comunión", "Confirmación", etc.
        disponibilidad: List[str] = None,  # ej: ["Sábados 9am", "Domingos 3pm"]
        activo: bool = True,
        notas: str = ""
    ) -> dict:
        """
        Estructura para un documento de catequista.
        
        Args:
            nombre: Nombre del catequista
            apellido: Apellido del catequista
            correo: Email de contacto
            edad: Edad del catequista
            telefono: Teléfono de contacto
            parroquia_id: ID de la parroquia a la que pertenece
            grupos_ids: Lista de IDs de grupos que imparte
            cedula: Número de cédula/identificación
            direccion: Dirección de residencia
            fecha_inicio: Fecha en que comenzó como catequista
            especialidad: Sacramento o nivel en el que se especializa
            disponibilidad: Horarios disponibles
            activo: Si el catequista está activo
            notas: Observaciones adicionales
        """
        return {
            "nombre": nombre,
            "apellido": apellido,
            "nombre_completo": f"{nombre} {apellido}",
            "correo": correo.lower(),
            "edad": edad,
            "telefono": telefono,
            "cedula": cedula,
            "direccion": direccion,
            "parroquia_id": parroquia_id,
            "grupos_ids": grupos_ids or [],
            "fecha_inicio": fecha_inicio or datetime.now(),
            "especialidad": especialidad,
            "disponibilidad": disponibilidad or [],
            "activo": activo,
            "notas": notas,
            "fecha_creacion": datetime.now(),
            "fecha_actualizacion": datetime.now()
        }
    
    @staticmethod
    def grupo_schema(
        numero_grupo: int,
        parroquia_id: str,  # Referencia a parroquias
        catequista_id: str,  # Referencia a catequista
        sacramento: str,  # ej: "Primera Comunión", "Confirmación", "Bautismo"
        numero_estudiantes: int = 0,
        nivel: str = "",  # ej: "Nivel 1", "Nivel 2", etc.
        horario: str = "",  # ej: "Sábados 9:00 AM - 11:00 AM"
        aula: str = "",  # Ubicación física
        año_lectivo: str = "",  # ej: "2025-2026"
        cupo_maximo: int = 30,
        catequizandos_ids: List[str] = None,  # Lista de IDs de catequizandos
        activo: bool = True,
        notas: str = ""
    ) -> dict:
        """
        Estructura para un documento de grupo.
        
        Args:
            numero_grupo: Número identificador del grupo
            parroquia_id: ID de la parroquia
            catequista_id: ID del catequista que imparte
            sacramento: Sacramento que se prepara
            numero_estudiantes: Cantidad de estudiantes inscritos
            nivel: Nivel o grado del grupo
            horario: Horario de clases
            aula: Salón o ubicación
            año_lectivo: Año académico
            cupo_maximo: Capacidad máxima del grupo
            catequizandos_ids: Lista de IDs de estudiantes
            activo: Si el grupo está activo
            notas: Observaciones
        """
        return {
            "numero_grupo": numero_grupo,
            "nombre_grupo": f"Grupo {numero_grupo} - {sacramento}",
            "parroquia_id": parroquia_id,
            "catequista_id": catequista_id,
            "sacramento": sacramento,
            "nivel": nivel,
            "numero_estudiantes": numero_estudiantes,
            "cupo_maximo": cupo_maximo,
            "cupos_disponibles": cupo_maximo - numero_estudiantes,
            "horario": horario,
            "aula": aula,
            "año_lectivo": año_lectivo,
            "catequizandos_ids": catequizandos_ids or [],
            "activo": activo,
            "notas": notas,
            "fecha_creacion": datetime.now(),
            "fecha_actualizacion": datetime.now()
        }
    
    @staticmethod
    def parroquia_schema(
        nombre: str,
        nombre_vicaria: str,
        ubicacion: dict,  # {"direccion": "", "ciudad": "", "provincia": "", "coordenadas": {"lat": 0, "lng": 0}}
        telefono: str,
        parroco: str = "",  # Nombre del párroco
        correo: str = "",
        horarios_misa: List[str] = None,  # ej: ["Lunes 7:00 AM", "Domingo 10:00 AM"]
        servicios: List[str] = None,  # ej: ["Bautismo", "Matrimonio", "Confirmación"]
        capacidad_catequesis: int = 0,
        activo: bool = True,
        notas: str = ""
    ) -> dict:
        """
        Estructura para un documento de parroquia.
        
        Args:
            nombre: Nombre de la parroquia
            nombre_vicaria: Nombre de la vicaría a la que pertenece
            ubicacion: Diccionario con dirección, ciudad, provincia y coordenadas
            telefono: Teléfono de contacto
            parroco: Nombre del párroco
            correo: Email de contacto
            horarios_misa: Lista de horarios de misas
            servicios: Sacramentos/servicios que ofrece
            capacidad_catequesis: Capacidad total para catequesis
            activo: Si la parroquia está activa
            notas: Observaciones
        """
        return {
            "nombre": nombre,
            "nombre_vicaria": nombre_vicaria,
            "ubicacion": ubicacion,
            "telefono": telefono,
            "parroco": parroco,
            "correo": correo.lower() if correo else "",
            "horarios_misa": horarios_misa or [],
            "servicios": servicios or ["Bautismo", "Primera Comunión", "Confirmación"],
            "capacidad_catequesis": capacidad_catequesis,
            "activo": activo,
            "notas": notas,
            "fecha_creacion": datetime.now(),
            "fecha_actualizacion": datetime.now()
        }
    
    @staticmethod
    def catequizando_schema(
        nombre: str,
        apellido: str,
        fecha_nacimiento: datetime,
        telefono: str,
        correo: str,
        parroquia_id: str,  # Referencia a parroquias
        grupo_id: str,  # Referencia a grupos
        nivel: str,  # Nivel de catequesis
        cedula: str = "",
        direccion: str = "",
        nombre_padre: str = "",
        nombre_madre: str = "",
        telefono_padres: str = "",
        padrino: dict = None,  # {"nombre": "", "telefono": "", "parroquia_bautismo": ""}
        madrina: dict = None,  # {"nombre": "", "telefono": "", "parroquia_bautismo": ""}
        certificados: List[dict] = None,  # [{"tipo": "Bautismo", "fecha": "", "parroquia": ""}]
        sacramentos_recibidos: List[str] = None,  # ["Bautismo", "Primera Comunión"]
        fecha_inscripcion: datetime = None,
        observaciones_medicas: str = "",
        activo: bool = True,
        notas: str = ""
    ) -> dict:
        """
        Estructura para un documento de catequizando.
        
        Args:
            nombre: Nombre del catequizando
            apellido: Apellido del catequizando
            fecha_nacimiento: Fecha de nacimiento
            telefono: Teléfono personal
            correo: Email del catequizando
            parroquia_id: ID de la parroquia a la que asiste
            grupo_id: ID del grupo al que pertenece
            nivel: Nivel de catequesis
            cedula: Número de cédula/identificación
            direccion: Dirección de residencia
            nombre_padre: Nombre completo del padre
            nombre_madre: Nombre completo de la madre
            telefono_padres: Teléfono de contacto de padres
            padrino: Información del padrino
            madrina: Información de la madrina
            certificados: Lista de certificados de sacramentos
            sacramentos_recibidos: Lista de sacramentos ya recibidos
            fecha_inscripcion: Fecha de inscripción
            observaciones_medicas: Alergias, condiciones especiales
            activo: Si está activo en catequesis
            notas: Observaciones adicionales
        """
        edad = datetime.now().year - fecha_nacimiento.year
        
        return {
            "nombre": nombre,
            "apellido": apellido,
            "nombre_completo": f"{nombre} {apellido}",
            "cedula": cedula,
            "fecha_nacimiento": fecha_nacimiento,
            "edad": edad,
            "telefono": telefono,
            "correo": correo.lower(),
            "direccion": direccion,
            "nombre_padre": nombre_padre,
            "nombre_madre": nombre_madre,
            "telefono_padres": telefono_padres,
            "padrino": padrino or {"nombre": "", "telefono": "", "parroquia_bautismo": ""},
            "madrina": madrina or {"nombre": "", "telefono": "", "parroquia_bautismo": ""},
            "parroquia_id": parroquia_id,
            "grupo_id": grupo_id,
            "nivel": nivel,
            "certificados": certificados or [],
            "sacramentos_recibidos": sacramentos_recibidos or [],
            "fecha_inscripcion": fecha_inscripcion or datetime.now(),
            "observaciones_medicas": observaciones_medicas,
            "activo": activo,
            "notas": notas,
            "fecha_creacion": datetime.now(),
            "fecha_actualizacion": datetime.now()
        }


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo de creación de documentos
    schemas = SchemasCatequesis()
    
    # Crear una parroquia de ejemplo
    parroquia = schemas.parroquia_schema(
        nombre="Parroquia San José",
        nombre_vicaria="Vicaría Norte",
        ubicacion={
            "direccion": "Av. Principal 123",
            "ciudad": "Quito",
            "provincia": "Pichincha",
            "coordenadas": {"lat": -0.1865, "lng": -78.4305}
        },
        telefono="02-2345678",
        parroco="Padre Juan Pérez",
        correo="sanjose@ejemplo.com"
    )
    
    print("Ejemplo de documento parroquia:")
    print(parroquia)
