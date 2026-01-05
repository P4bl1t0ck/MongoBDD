# 📖 Sistema de Gestión de Catequesis - CatequesisDB

## 🎯 Descripción
Sistema web completo para la gestión de catequesis en parroquias, desarrollado con Flask (Python) y MongoDB.

## ✅ Características Implementadas

### Backend (Flask + Python)
- ✅ API RESTful completa con Flask
- ✅ Conexión a MongoDB Atlas
- ✅ CRUD completo para 4 colecciones:
  - Parroquias
  - Catequistas  
  - Grupos
  - Catequizandos
- ✅ Endpoints de reportes y estadísticas
- ✅ Manejo de errores y validaciones
- ✅ CORS habilitado para frontend

### Frontend (HTML + CSS + JavaScript)
- ✅ Interfaz web moderna y responsiva
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Formularios completos para cada entidad
- ✅ Tablas dinámicas con datos
- ✅ Sistema de navegación por tabs
- ✅ Modales para mensajes de confirmación
- ✅ Búsquedas y filtros
- ✅ Reportes visuales

### Base de Datos (MongoDB)
- ✅ 4 Colecciones estructuradas:
  - **parroquias**: Información de parroquias y ubicaciones
  - **catequistas**: Datos de catequistas y especialidades
  - **grupos**: Grupos de catequesis con horarios y cupos
  - **catequizandos**: Registro completo de estudiantes
- ✅ Relaciones entre colecciones
- ✅ Validación de datos
- ✅ Campos calculados automáticos

## 🚀 Instalación y Configuración

### 1. Requisitos Previos
- Python 3.8 o superior
- MongoDB Atlas (cuenta gratuita)
- Navegador web moderno

### 2. Instalar Dependencias

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Conexión a MongoDB

El string de conexión está configurado en:
```
Backend/app_catequesis.py
```

### 4. Ejecutar el Servidor

**Windows:**
```bash
cd Backend
python app_catequesis.py
```

**macOS/Linux:**
```bash
cd Backend
python3 app_catequesis.py
```

### 5. Acceder a la Aplicación

Abre tu navegador y ve a:
```
http://localhost:5001
```

## 📁 Estructura del Proyecto

```
MongoBDD/
├── Backend/
│   ├── app_catequesis.py      # Servidor Flask principal
│   ├── conection.py            # Clase de conexión a MongoDB
│   ├── schemas.py              # Esquemas de datos
│   ├── ejemplo_catequesis.py   # Script de ejemplo con datos
│   └── test_crud_mongo.py      # Tests
├── Frontend/
│   ├── index.html              # Interfaz web principal
│   ├── styles.css              # Estilos CSS
│   └── app.js                  # Lógica JavaScript
└── requirements.txt            # Dependencias Python
```

## 🔧 Funcionalidades Principales

### 1. Gestión de Parroquias
- Registrar parroquias con ubicación, contacto y capacidad
- Ver listado de todas las parroquias
- Eliminar parroquias

### 2. Gestión de Catequistas
- Registrar catequistas con datos personales y especialidad
- Asignar catequistas a parroquias
- Ver listado y eliminar

### 3. Gestión de Grupos
- Crear grupos de catequesis
- Asignar catequista y parroquia
- Definir horarios, cupos y sacramento
- Control automático de cupos disponibles

### 4. Gestión de Catequizandos (PRINCIPAL)
- **Registro completo de catequizandos**
  - Datos personales (nombre, cédula, fecha nacimiento)
  - Datos de padres
  - Datos de padrinos
  - Asignación a grupo y parroquia
  - Nivel de catequesis
- **Consultas principales**
  - Listar todos los catequizandos
  - Filtrar por grupo
  - Búsqueda por nombre
  - Ver detalles completos

### 5. Reportes y Consultas
- Estadísticas generales del sistema
- Catequizandos por sacramento
- Búsqueda avanzada
- Dashboard con métricas en tiempo real

## 📊 API Endpoints

### Parroquias
```
GET    /api/parroquias          # Listar todas
POST   /api/parroquias          # Crear nueva
GET    /api/parroquias/<id>     # Obtener por ID
PUT    /api/parroquias/<id>     # Actualizar
DELETE /api/parroquias/<id>     # Eliminar
```

### Catequistas
```
GET    /api/catequistas?parroquia_id=<id>
POST   /api/catequistas
GET    /api/catequistas/<id>
PUT    /api/catequistas/<id>
DELETE /api/catequistas/<id>
```

### Grupos
```
GET    /api/grupos?parroquia_id=<id>
POST   /api/grupos
GET    /api/grupos/<id>
PUT    /api/grupos/<id>
DELETE /api/grupos/<id>
```

### Catequizandos
```
GET    /api/catequizandos?grupo_id=<id>&parroquia_id=<id>
POST   /api/catequizandos
GET    /api/catequizandos/<id>
PUT    /api/catequizandos/<id>
DELETE /api/catequizandos/<id>
```

### Reportes
```
GET    /api/estadisticas
GET    /api/reportes/por-sacramento
GET    /api/health
```

## 🎨 Tecnologías Utilizadas

### Backend
- **Python 3.x**
- **Flask 3.0.0** - Framework web
- **PyMongo 4.15.5** - Driver de MongoDB
- **Flask-CORS 4.0.0** - Manejo de CORS

### Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos modernos y responsivos
- **JavaScript ES6+** - Lógica de negocio
- **Fetch API** - Comunicación con backend

### Base de Datos
- **MongoDB Atlas** - Base de datos NoSQL en la nube

## 📝 Ejemplo de Uso

### 1. Registrar una Parroquia
1. Ir a la pestaña "⛪ Parroquias"
2. Llenar el formulario con los datos
3. Hacer clic en "💾 Guardar Parroquia"

### 2. Registrar un Catequizando
1. Asegurarse de tener al menos una parroquia y un grupo
2. Ir a "👦 Catequizandos"
3. Llenar todos los campos del formulario:
   - Datos personales
   - Datos de padres
   - Datos de padrinos
   - Seleccionar parroquia y grupo
4. Hacer clic en "💾 Registrar Catequizando"

### 3. Ver Reportes
1. Ir a "📈 Reportes"
2. Ver estadísticas generales
3. Hacer clic en "🔄 Generar Reporte" para ver catequizandos por sacramento
4. Usar la búsqueda avanzada para encontrar estudiantes

## 🔍 Consultas Principales Implementadas

1. **Listar todos los catequizandos** con sus datos completos
2. **Filtrar catequizandos por grupo**
3. **Buscar catequizandos por nombre**
4. **Estadísticas generales** del sistema
5. **Reporte de catequizandos por sacramento**
6. **Conteo automático de estudiantes por grupo**

## ⚠️ Notas Importantes

- El sistema actualiza automáticamente el contador de estudiantes cuando se registra un catequizando
- Los cupos disponibles se calculan automáticamente
- Todas las operaciones muestran mensajes de confirmación
- Los datos se guardan directamente en MongoDB Atlas

## 🛠️ Desarrollo Futuro

Posibles mejoras:
- Autenticación de usuarios
- Exportación de reportes a PDF/Excel
- Sistema de asistencia
- Notificaciones por email
- Gestión de certificados
- Calendario de eventos

## 👥 Autor

Desarrollado como proyecto de Base de Datos con MongoDB

## 📄 Licencia

Proyecto educativo - 2026
