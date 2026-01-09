/*
=============================================================================
  SISTEMA DE GESTIÓN DE CATEQUESIS - MONGODB CRUD OPERATIONS
=============================================================================
  Archivo JavaScript completo con operaciones CRUD para MongoDB
  Base de Datos: CatequesisDB
  Colecciones: parroquias, catequistas, grupos, catequizandos
  
  Basado en: https://www.youtube.com/watch?v=WUok6mcBhjI
  
  INSTRUCCIONES:
  1. Ejecutar en MongoDB Shell o MongoDB Compass
  2. Asegurarse de tener MongoDB instalado y corriendo
  3. Modificar la URI de conexión según sea necesario
=============================================================================
*/

// =============================================================================
// CONFIGURACIÓN Y CONEXIÓN A LA BASE DE DATOS
// =============================================================================

// URI de conexión a MongoDB (modificar según tu configuración)
const MONGO_URI = "mongodb+srv://AdminUdla:UDLA@clusterpablutus.hneadkh.mongodb.net/?appName=ClusterPablutus";
const DB_NAME = "CatequesisDB";

// En MongoDB Shell, usar:
// use CatequesisDB

print("\n=== INICIANDO SISTEMA DE GESTIÓN DE CATEQUESIS ===\n");

// =============================================================================
// 1. CREACIÓN DE LA BASE DE DATOS Y COLECCIONES
// =============================================================================

print("=== PASO 1: CREACIÓN DE COLECCIONES ===\n");

// Crear la base de datos (se crea automáticamente al insertar el primer documento)
// use CatequesisDB  // Descomentar si se ejecuta directamente en MongoDB Shell

// Crear colecciones con validación de esquema
db.createCollection("parroquias", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nombre", "nombre_vicaria", "ubicacion", "telefono", "activo"],
      properties: {
        nombre: {
          bsonType: "string",
          description: "Nombre de la parroquia - requerido"
        },
        nombre_vicaria: {
          bsonType: "string",
          description: "Nombre de la vicaría - requerido"
        },
        ubicacion: {
          bsonType: "object",
          required: ["direccion", "ciudad", "provincia"],
          properties: {
            direccion: { bsonType: "string" },
            ciudad: { bsonType: "string" },
            provincia: { bsonType: "string" },
            coordenadas: {
              bsonType: "object",
              properties: {
                lat: { bsonType: "double" },
                lng: { bsonType: "double" }
              }
            }
          }
        },
        telefono: {
          bsonType: "string",
          description: "Teléfono de contacto - requerido"
        },
        parroco: {
          bsonType: "string",
          description: "Nombre del párroco"
        },
        correo: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
          description: "Email válido"
        },
        horarios_misa: {
          bsonType: "array",
          items: { bsonType: "string" }
        },
        servicios: {
          bsonType: "array",
          items: { bsonType: "string" }
        },
        capacidad_catequesis: {
          bsonType: "int",
          minimum: 0
        },
        activo: {
          bsonType: "bool",
          description: "Estado de la parroquia - requerido"
        }
      }
    }
  }
});

db.createCollection("catequistas", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nombre", "apellido", "correo", "telefono", "parroquia_id", "activo"],
      properties: {
        nombre: { bsonType: "string" },
        apellido: { bsonType: "string" },
        nombre_completo: { bsonType: "string" },
        correo: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        edad: {
          bsonType: "int",
          minimum: 18,
          maximum: 100
        },
        telefono: { bsonType: "string" },
        cedula: { bsonType: "string" },
        direccion: { bsonType: "string" },
        parroquia_id: { bsonType: "string" },
        grupos_ids: {
          bsonType: "array",
          items: { bsonType: "string" }
        },
        fecha_inicio: { bsonType: "date" },
        especialidad: { bsonType: "string" },
        disponibilidad: {
          bsonType: "array",
          items: { bsonType: "string" }
        },
        activo: { bsonType: "bool" }
      }
    }
  }
});

db.createCollection("grupos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["numero_grupo", "parroquia_id", "catequista_id", "sacramento", "activo"],
      properties: {
        numero_grupo: {
          bsonType: "int",
          minimum: 1
        },
        nombre_grupo: { bsonType: "string" },
        parroquia_id: { bsonType: "string" },
        catequista_id: { bsonType: "string" },
        sacramento: {
          bsonType: "string",
          enum: ["Bautismo", "Primera Comunión", "Confirmación", "Matrimonio"]
        },
        nivel: { bsonType: "string" },
        numero_estudiantes: {
          bsonType: "int",
          minimum: 0
        },
        cupo_maximo: {
          bsonType: "int",
          minimum: 1
        },
        horario: { bsonType: "string" },
        aula: { bsonType: "string" },
        año_lectivo: { bsonType: "string" },
        catequizandos_ids: {
          bsonType: "array",
          items: { bsonType: "string" }
        },
        activo: { bsonType: "bool" }
      }
    }
  }
});

db.createCollection("catequizandos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nombre", "apellido", "fecha_nacimiento", "telefono", "correo", "parroquia_id", "grupo_id", "nivel", "activo"],
      properties: {
        nombre: { bsonType: "string" },
        apellido: { bsonType: "string" },
        nombre_completo: { bsonType: "string" },
        cedula: { bsonType: "string" },
        fecha_nacimiento: { bsonType: "date" },
        edad: {
          bsonType: "int",
          minimum: 0,
          maximum: 100
        },
        telefono: { bsonType: "string" },
        correo: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        direccion: { bsonType: "string" },
        nombre_padre: { bsonType: "string" },
        nombre_madre: { bsonType: "string" },
        telefono_padres: { bsonType: "string" },
        padrino: { bsonType: "object" },
        madrina: { bsonType: "object" },
        parroquia_id: { bsonType: "string" },
        grupo_id: { bsonType: "string" },
        nivel: { bsonType: "string" },
        certificados: {
          bsonType: "array",
          items: { bsonType: "object" }
        },
        sacramentos_recibidos: {
          bsonType: "array",
          items: { bsonType: "string" }
        },
        fecha_inscripcion: { bsonType: "date" },
        observaciones_medicas: { bsonType: "string" },
        activo: { bsonType: "bool" }
      }
    }
  }
});

print("✓ Colecciones creadas exitosamente\n");

// =============================================================================
// 2. CREAR ÍNDICES PARA MEJORAR EL RENDIMIENTO
// =============================================================================

print("=== PASO 2: CREACIÓN DE ÍNDICES ===\n");

// Índices para Parroquias
db.parroquias.createIndex({ "nombre": 1 }, { unique: true });
db.parroquias.createIndex({ "nombre_vicaria": 1 });
db.parroquias.createIndex({ "activo": 1 });
db.parroquias.createIndex({ "ubicacion.ciudad": 1 });

// Índices para Catequistas
db.catequistas.createIndex({ "correo": 1 }, { unique: true });
db.catequistas.createIndex({ "cedula": 1 }, { unique: true, sparse: true });
db.catequistas.createIndex({ "parroquia_id": 1 });
db.catequistas.createIndex({ "activo": 1 });
db.catequistas.createIndex({ "nombre": 1, "apellido": 1 });

// Índices para Grupos
db.grupos.createIndex({ "numero_grupo": 1, "parroquia_id": 1 }, { unique: true });
db.grupos.createIndex({ "parroquia_id": 1 });
db.grupos.createIndex({ "catequista_id": 1 });
db.grupos.createIndex({ "sacramento": 1 });
db.grupos.createIndex({ "activo": 1 });
db.grupos.createIndex({ "año_lectivo": 1 });

// Índices para Catequizandos
db.catequizandos.createIndex({ "cedula": 1 }, { unique: true });
db.catequizandos.createIndex({ "correo": 1 }, { unique: true });
db.catequizandos.createIndex({ "parroquia_id": 1 });
db.catequizandos.createIndex({ "grupo_id": 1 });
db.catequizandos.createIndex({ "activo": 1 });
db.catequizandos.createIndex({ "nombre": 1, "apellido": 1 });
db.catequizandos.createIndex({ "sacramentos_recibidos": 1 });

print("✓ Índices creados exitosamente\n");

// =============================================================================
// 3. OPERACIONES CREATE (INSERTAR DATOS)
// =============================================================================

print("=== PASO 3: INSERCIÓN DE DATOS (CREATE) ===\n");

// --- 3.1 INSERTAR PARROQUIAS ---
print("Insertando parroquias...");

db.parroquias.insertMany([
  {
    "_id": "PAR001",
    "nombre": "San José",
    "nombre_vicaria": "Vicaría Norte",
    "ubicacion": {
      "direccion": "Av. Principal 123",
      "ciudad": "Quito",
      "provincia": "Pichincha",
      "coordenadas": { "lat": -0.1865, "lng": -78.4305 }
    },
    "telefono": "0987654321",
    "parroco": "Padre Juan Pérez",
    "correo": "sanjose@parroquia.ec",
    "horarios_misa": ["Lunes a Viernes 7:00 AM", "Sábados 6:00 PM", "Domingos 8:00 AM, 10:00 AM, 12:00 PM"],
    "servicios": ["Bautismo", "Primera Comunión", "Confirmación", "Matrimonio"],
    "capacidad_catequesis": 200,
    "activo": true,
    "notas": "",
    "fecha_creacion": new Date("2026-01-09T01:30:28.943Z"),
    "fecha_actualizacion": new Date("2026-01-09T01:30:28.943Z")
  },
  {
    "_id": "PAR002",
    "nombre": "Santa María",
    "nombre_vicaria": "Vicaría Sur",
    "ubicacion": {
      "direccion": "Calle Flores 456",
      "ciudad": "Quito",
      "provincia": "Pichincha",
      "coordenadas": { "lat": -0.2500, "lng": -78.5200 }
    },
    "telefono": "0987654322",
    "parroco": "Padre Carlos Mendoza",
    "correo": "santamaria@parroquia.ec",
    "horarios_misa": ["Lunes a Viernes 6:30 AM", "Sábados 7:00 PM", "Domingos 9:00 AM, 11:00 AM"],
    "servicios": ["Bautismo", "Primera Comunión", "Confirmación"],
    "capacidad_catequesis": 200,
    "activo": true,
    "notas": "",
    "fecha_creacion": new Date("2026-01-09T01:30:28.943Z"),
    "fecha_actualizacion": new Date("2026-01-09T01:30:28.943Z")
  }
]);

print("✓ Parroquias insertadas\n");

// --- 3.2 INSERTAR CATEQUISTAS ---
print("Insertando catequistas...");

db.catequistas.insertMany([
  {
    "_id": "CAT001",
    "nombre": "María Elena",
    "apellido": "Rodríguez",
    "nombre_completo": "María Elena Rodríguez",
    "correo": "maria.rodriguez@catequesis.com",
    "edad": 45,
    "telefono": "0998877665",
    "cedula": "1712345678",
    "direccion": "Av. 6 de Diciembre N24-123",
    "parroquia_id": "PAR001",
    "grupos_ids": ["GRP2024A"],
    "fecha_inicio": new Date("2020-01-15T00:00:00.000Z"),
    "especialidad": "Primera Comunión",
    "disponibilidad": ["Sábados 3:00 PM", "Domingos 10:00 AM"],
    "activo": true,
    "notas": "Coordinadora general de catequesis",
    "fecha_creacion": new Date("2026-01-09T01:33:16.767Z"),
    "fecha_actualizacion": new Date("2026-01-09T01:33:16.767Z")
  },
  {
    "_id": "CAT002",
    "nombre": "Juan Carlos",
    "apellido": "Martínez",
    "nombre_completo": "Juan Carlos Martínez",
    "correo": "juan.martinez@catequesis.com",
    "edad": 38,
    "telefono": "0998877666",
    "cedula": "1723456789",
    "direccion": "Calle García Moreno 456",
    "parroquia_id": "PAR001",
    "grupos_ids": ["GRP2024B"],
    "fecha_inicio": new Date("2021-03-10T00:00:00.000Z"),
    "especialidad": "Confirmación",
    "disponibilidad": ["Sábados 5:00 PM", "Domingos 3:00 PM"],
    "activo": true,
    "notas": "",
    "fecha_creacion": new Date("2026-01-09T01:33:16.767Z"),
    "fecha_actualizacion": new Date("2026-01-09T01:33:16.767Z")
  }
]);

print("✓ Catequistas insertados\n");

// --- 3.3 INSERTAR GRUPOS ---
print("Insertando grupos...");

db.grupos.insertMany([
  {
    "_id": "GRP2024A",
    "numero_grupo": 1,
    "nombre_grupo": "Grupo 1 - Primera Comunión",
    "parroquia_id": "PAR001",
    "catequista_id": "CAT001",
    "sacramento": "Primera Comunión",
    "nivel": "Nivel 2",
    "numero_estudiantes": 0,
    "cupo_maximo": 30,
    "cupos_disponibles": 30,
    "horario": "Sábados 3:00 PM - 5:00 PM",
    "aula": "Salón 101",
    "año_lectivo": "2024-2025",
    "catequizandos_ids": [],
    "activo": true,
    "notas": "Grupo de Primera Comunión para niños de 9-11 años",
    "fecha_creacion": new Date("2024-01-01T00:00:00.000Z"),
    "fecha_actualizacion": new Date("2024-01-01T00:00:00.000Z")
  },
  {
    "_id": "GRP2024B",
    "numero_grupo": 2,
    "nombre_grupo": "Grupo 2 - Confirmación",
    "parroquia_id": "PAR001",
    "catequista_id": "CAT002",
    "sacramento": "Confirmación",
    "nivel": "Nivel 1",
    "numero_estudiantes": 0,
    "cupo_maximo": 25,
    "cupos_disponibles": 25,
    "horario": "Sábados 5:00 PM - 7:00 PM",
    "aula": "Salón 102",
    "año_lectivo": "2024-2025",
    "catequizandos_ids": [],
    "activo": true,
    "notas": "Grupo de Confirmación para adolescentes",
    "fecha_creacion": new Date("2024-01-01T00:00:00.000Z"),
    "fecha_actualizacion": new Date("2024-01-01T00:00:00.000Z")
  }
]);

print("✓ Grupos insertados\n");

// --- 3.4 INSERTAR UN CATEQUIZANDO ---
print("Insertando catequizando de ejemplo...");

db.catequizandos.insertOne({
  "_id": "CZO001",
  "nombre": "Mateo",
  "apellido": "López",
  "nombre_completo": "Mateo López",
  "cedula": "1750123456",
  "fecha_nacimiento": new Date("2015-05-10T00:00:00.000Z"),
  "edad": 10,
  "telefono": "0991234567",
  "correo": "mateo.lopez@estudiante.ec",
  "direccion": "Av. Los Shyris 234",
  "nombre_padre": "Carlos López Morales",
  "nombre_madre": "Patricia Sánchez Vega",
  "telefono_padres": "0991234567",
  "padrino": {
    "nombre": "Roberto López",
    "telefono": "0991234500",
    "parroquia_bautismo": "PAR001"
  },
  "madrina": {
    "nombre": "Sandra Morales",
    "telefono": "0991234501",
    "parroquia_bautismo": "PAR001"
  },
  "parroquia_id": "PAR001",
  "grupo_id": "GRP2024A",
  "nivel": "Primera Comunión - Nivel 2",
  "certificados": [
    {
      "tipo": "Bautismo",
      "fecha": new Date("2015-08-15T00:00:00.000Z"),
      "parroquia": "PAR001",
      "libro": "12",
      "folio": "45",
      "numero": "123"
    }
  ],
  "sacramentos_recibidos": ["Bautismo"],
  "fecha_inscripcion": new Date("2024-01-15T00:00:00.000Z"),
  "observaciones_medicas": "",
  "activo": true,
  "notas": "Estudiante aplicado",
  "fecha_creacion": new Date("2024-01-15T00:00:00.000Z"),
  "fecha_actualizacion": new Date("2024-01-15T00:00:00.000Z")
});

print("✓ Catequizando insertado\n");

// =============================================================================
// 4. OPERACIONES READ (CONSULTAR DATOS)
// =============================================================================

print("\n=== PASO 4: CONSULTAS (READ) ===\n");

// --- 4.1 CONSULTAS BÁSICAS ---
print("--- Consultas Básicas ---\n");

// Obtener todas las parroquias
print("1. Todas las parroquias:");
db.parroquias.find().pretty();

// Obtener una parroquia específica
print("\n2. Parroquia 'San José':");
db.parroquias.findOne({ nombre: "San José" });

// Contar documentos
print("\n3. Total de catequistas:");
print(db.catequistas.count());

// --- 4.2 CONSULTAS CON FILTROS ---
print("\n--- Consultas con Filtros ---\n");

// Catequistas activos de una parroquia específica
print("1. Catequistas activos de PAR001:");
db.catequistas.find({ 
  parroquia_id: "PAR001",
  activo: true 
}).pretty();

// Grupos con cupos disponibles
print("\n2. Grupos con cupos disponibles:");
db.grupos.find({ 
  cupos_disponibles: { $gt: 0 },
  activo: true 
}).pretty();

// Catequizandos por rango de edad
print("\n3. Catequizandos entre 9 y 11 años:");
db.catequizandos.find({
  edad: { $gte: 9, $lte: 11 }
}).pretty();

// --- 4.3 CONSULTAS CON PROYECCIÓN ---
print("\n--- Consultas con Proyección ---\n");

// Solo nombres y correos de catequistas
print("1. Nombres y correos de catequistas:");
db.catequistas.find(
  {},
  { nombre_completo: 1, correo: 1, _id: 0 }
).pretty();

// --- 4.4 CONSULTAS CON ORDENAMIENTO ---
print("\n--- Consultas con Ordenamiento ---\n");

// Catequizandos ordenados por edad (descendente)
print("1. Catequizandos por edad (mayor a menor):");
db.catequizandos.find().sort({ edad: -1 }).pretty();

// Grupos ordenados alfabéticamente
print("\n2. Grupos ordenados alfabéticamente:");
db.grupos.find().sort({ nombre_grupo: 1 }).pretty();

// --- 4.5 CONSULTAS CON LIMIT Y SKIP ---
print("\n--- Consultas con Paginación ---\n");

// Primeros 5 catequizandos
print("1. Primeros 5 catequizandos:");
db.catequizandos.find().limit(5).pretty();

// Siguiente página (saltando los primeros 5)
print("\n2. Siguiente página:");
db.catequizandos.find().skip(5).limit(5).pretty();

// --- 4.6 CONSULTAS CON OPERADORES LÓGICOS ---
print("\n--- Consultas con Operadores Lógicos ---\n");

// Catequistas de PAR001 O PAR002
print("1. Catequistas de PAR001 o PAR002:");
db.catequistas.find({
  $or: [
    { parroquia_id: "PAR001" },
    { parroquia_id: "PAR002" }
  ]
}).pretty();

// Grupos de Primera Comunión Y con cupos disponibles
print("\n2. Grupos de Primera Comunión con cupos:");
db.grupos.find({
  $and: [
    { sacramento: "Primera Comunión" },
    { cupos_disponibles: { $gt: 0 } }
  ]
}).pretty();

// --- 4.7 CONSULTAS EN ARRAYS ---
print("\n--- Consultas en Arrays ---\n");

// Catequizandos que han recibido Bautismo
print("1. Catequizandos bautizados:");
db.catequizandos.find({
  sacramentos_recibidos: "Bautismo"
}).pretty();

// Parroquias que ofrecen Matrimonio
print("\n2. Parroquias que ofrecen Matrimonio:");
db.parroquias.find({
  servicios: "Matrimonio"
}).pretty();

// --- 4.8 CONSULTAS ANIDADAS ---
print("\n--- Consultas en Campos Anidados ---\n");

// Parroquias en Quito
print("1. Parroquias en Quito:");
db.parroquias.find({
  "ubicacion.ciudad": "Quito"
}).pretty();

// --- 4.9 CONSULTAS CON REGEX ---
print("\n--- Consultas con Expresiones Regulares ---\n");

// Catequistas cuyo nombre empieza con 'M'
print("1. Catequistas con nombre que empieza con 'M':");
db.catequistas.find({
  nombre: /^M/
}).pretty();

// Correos que contienen 'catequesis'
print("\n2. Correos que contienen 'catequesis':");
db.catequistas.find({
  correo: /catequesis/i
}).pretty();

// --- 4.10 AGREGACIONES SIMPLES ---
print("\n--- Agregaciones ---\n");

// Agrupar catequizandos por parroquia y contar
print("1. Catequizandos por parroquia:");
db.catequizandos.aggregate([
  {
    $group: {
      _id: "$parroquia_id",
      total: { $sum: 1 },
      promedio_edad: { $avg: "$edad" }
    }
  }
]).pretty();

// Grupos por sacramento
print("\n2. Grupos por sacramento:");
db.grupos.aggregate([
  {
    $group: {
      _id: "$sacramento",
      total_grupos: { $sum: 1 },
      total_estudiantes: { $sum: "$numero_estudiantes" },
      cupos_totales: { $sum: "$cupo_maximo" }
    }
  }
]).pretty();

// =============================================================================
// 5. OPERACIONES UPDATE (ACTUALIZAR DATOS)
// =============================================================================

print("\n=== PASO 5: ACTUALIZACIONES (UPDATE) ===\n");

// --- 5.1 ACTUALIZAR UN DOCUMENTO ---
print("--- Actualizar un Documento ---\n");

// Actualizar teléfono de un catequista
print("1. Actualizando teléfono de catequista...");
db.catequistas.updateOne(
  { _id: "CAT001" },
  { 
    $set: { 
      telefono: "0998877999",
      fecha_actualizacion: new Date()
    }
  }
);
print("✓ Teléfono actualizado");

// Verificar actualización
print("\nCatequista actualizado:");
db.catequistas.findOne({ _id: "CAT001" });

// --- 5.2 ACTUALIZAR MÚLTIPLES DOCUMENTOS ---
print("\n--- Actualizar Múltiples Documentos ---\n");

// Actualizar todas las parroquias de una vicaría
print("1. Actualizando parroquias de Vicaría Norte...");
db.parroquias.updateMany(
  { nombre_vicaria: "Vicaría Norte" },
  { 
    $set: { 
      fecha_actualizacion: new Date()
    }
  }
);
print("✓ Parroquias actualizadas");

// --- 5.3 OPERADORES DE ACTUALIZACIÓN ---
print("\n--- Operadores de Actualización ---\n");

// $inc - Incrementar número de estudiantes
print("1. Incrementando estudiantes en un grupo...");
db.grupos.updateOne(
  { _id: "GRP2024A" },
  { 
    $inc: { numero_estudiantes: 1 },
    $set: { fecha_actualizacion: new Date() }
  }
);
print("✓ Estudiantes incrementados");

// $push - Agregar elemento a un array
print("\n2. Agregando grupo a catequista...");
db.catequistas.updateOne(
  { _id: "CAT001" },
  { 
    $push: { grupos_ids: "GRP2024C" }
  }
);
print("✓ Grupo agregado");

// $pull - Remover elemento de un array
print("\n3. Removiendo grupo de catequista...");
db.catequistas.updateOne(
  { _id: "CAT001" },
  { 
    $pull: { grupos_ids: "GRP2024C" }
  }
);
print("✓ Grupo removido");

// $addToSet - Agregar a array sin duplicados
print("\n4. Agregando sacramento a catequizando (sin duplicar)...");
db.catequizandos.updateOne(
  { _id: "CZO001" },
  { 
    $addToSet: { sacramentos_recibidos: "Primera Comunión" }
  }
);
print("✓ Sacramento agregado");

// $unset - Remover campo
print("\n5. Removiendo campo notas...");
db.grupos.updateOne(
  { _id: "GRP2024A" },
  { 
    $unset: { notas: "" }
  }
);
print("✓ Campo removido");

// $rename - Renombrar campo
print("\n6. Renombrando campo (ejemplo)...");
// db.parroquias.updateMany({}, { $rename: { "old_field": "new_field" } });

// --- 5.4 ACTUALIZACIÓN CON UPSERT ---
print("\n--- Upsert (Actualizar o Insertar) ---\n");

// Si existe actualiza, si no existe inserta
print("1. Upsert de un catequista...");
db.catequistas.updateOne(
  { cedula: "1799999999" },
  { 
    $set: {
      nombre: "Nuevo",
      apellido: "Catequista",
      nombre_completo: "Nuevo Catequista",
      correo: "nuevo@catequesis.com",
      telefono: "0999999999",
      parroquia_id: "PAR001",
      activo: true,
      fecha_creacion: new Date(),
      fecha_actualizacion: new Date()
    }
  },
  { upsert: true }
);
print("✓ Upsert completado");

// --- 5.5 ACTUALIZACIÓN DE CAMPOS ANIDADOS ---
print("\n--- Actualizar Campos Anidados ---\n");

// Actualizar coordenadas de ubicación
print("1. Actualizando coordenadas de parroquia...");
db.parroquias.updateOne(
  { _id: "PAR001" },
  { 
    $set: { 
      "ubicacion.coordenadas.lat": -0.1900,
      "ubicacion.coordenadas.lng": -78.4400
    }
  }
);
print("✓ Coordenadas actualizadas");

// --- 5.6 ACTUALIZACIÓN CON OPERADORES ARRAY ---
print("\n--- Actualización de Arrays ---\n");

// Actualizar un elemento específico del array
print("1. Actualizando horario de misa...");
db.parroquias.updateOne(
  { _id: "PAR001" },
  { 
    $set: { 
      "horarios_misa.0": "Lunes a Viernes 6:30 AM"
    }
  }
);
print("✓ Horario actualizado");

// =============================================================================
// 6. OPERACIONES DELETE (ELIMINAR DATOS)
// =============================================================================

print("\n=== PASO 6: ELIMINACIONES (DELETE) ===\n");

// --- 6.1 ELIMINAR UN DOCUMENTO ---
print("--- Eliminar un Documento ---\n");

// Primero insertar un documento de prueba
print("1. Insertando documento de prueba...");
db.catequistas.insertOne({
  "_id": "CAT999",
  "nombre": "Temporal",
  "apellido": "Test",
  "nombre_completo": "Temporal Test",
  "correo": "temporal@test.com",
  "telefono": "0999999999",
  "parroquia_id": "PAR001",
  "activo": false,
  "fecha_creacion": new Date()
});

// Eliminar el documento
print("2. Eliminando documento de prueba...");
db.catequistas.deleteOne({ _id: "CAT999" });
print("✓ Documento eliminado");

// --- 6.2 ELIMINAR MÚLTIPLES DOCUMENTOS ---
print("\n--- Eliminar Múltiples Documentos ---\n");

// Eliminar todos los catequistas inactivos (ejemplo, no ejecutar si hay datos reales)
print("1. Eliminando catequistas inactivos (ejemplo):");
// db.catequistas.deleteMany({ activo: false });
print("(Comentado para proteger datos)");

// --- 6.3 ELIMINACIÓN SEGURA (SOFT DELETE) ---
print("\n--- Eliminación Segura (Soft Delete) ---\n");

// En lugar de eliminar, marcar como inactivo
print("1. Desactivando en lugar de eliminar...");
db.catequistas.updateOne(
  { cedula: "1799999999" },
  { 
    $set: { 
      activo: false,
      fecha_eliminacion: new Date()
    }
  }
);
print("✓ Registro desactivado");

// =============================================================================
// 7. OPERACIONES AVANZADAS
// =============================================================================

print("\n=== PASO 7: OPERACIONES AVANZADAS ===\n");

// --- 7.1 TRANSACCIONES ---
print("--- Transacciones (Requiere Replica Set) ---\n");

// Ejemplo de transacción (comentado porque requiere replica set)
/*
const session = db.getMongo().startSession();
session.startTransaction();

try {
  // Operación 1: Inscribir catequizando
  session.getDatabase("CatequesisDB").catequizandos.insertOne({
    // ... datos del catequizando
  });
  
  // Operación 2: Actualizar cupos del grupo
  session.getDatabase("CatequesisDB").grupos.updateOne(
    { _id: "GRP2024A" },
    { $inc: { numero_estudiantes: 1, cupos_disponibles: -1 } }
  );
  
  // Si todo está bien, confirmar
  session.commitTransaction();
  print("✓ Transacción completada");
} catch (error) {
  // Si hay error, revertir
  session.abortTransaction();
  print("✗ Transacción revertida");
} finally {
  session.endSession();
}
*/

print("(Requiere configuración de Replica Set)");

// --- 7.2 AGREGACIONES COMPLEJAS ---
print("\n--- Agregaciones Complejas ---\n");

// Pipeline de agregación complejo
print("1. Estadísticas por parroquia:");
db.catequizandos.aggregate([
  // Etapa 1: Filtrar solo activos
  {
    $match: { activo: true }
  },
  // Etapa 2: Agrupar por parroquia
  {
    $group: {
      _id: "$parroquia_id",
      total_catequizandos: { $sum: 1 },
      edad_promedio: { $avg: "$edad" },
      edad_minima: { $min: "$edad" },
      edad_maxima: { $max: "$edad" }
    }
  },
  // Etapa 3: Ordenar por total descendente
  {
    $sort: { total_catequizandos: -1 }
  },
  // Etapa 4: Dar formato a los resultados
  {
    $project: {
      parroquia_id: "$_id",
      total_catequizandos: 1,
      edad_promedio: { $round: ["$edad_promedio", 1] },
      rango_edades: {
        $concat: [
          { $toString: "$edad_minima" },
          " - ",
          { $toString: "$edad_maxima" }
        ]
      },
      _id: 0
    }
  }
]).pretty();

// --- 7.3 LOOKUP (JOIN) ---
print("\n--- Lookup (Joins entre Colecciones) ---\n");

// Obtener grupos con información del catequista
print("1. Grupos con información de catequista:");
db.grupos.aggregate([
  {
    $lookup: {
      from: "catequistas",
      localField: "catequista_id",
      foreignField: "_id",
      as: "catequista_info"
    }
  },
  {
    $unwind: "$catequista_info"
  },
  {
    $project: {
      nombre_grupo: 1,
      sacramento: 1,
      horario: 1,
      "catequista_info.nombre_completo": 1,
      "catequista_info.telefono": 1,
      "catequista_info.correo": 1
    }
  }
]).pretty();

// Obtener parroquias con sus catequistas
print("\n2. Parroquias con lista de catequistas:");
db.parroquias.aggregate([
  {
    $lookup: {
      from: "catequistas",
      localField: "_id",
      foreignField: "parroquia_id",
      as: "catequistas"
    }
  },
  {
    $project: {
      nombre: 1,
      nombre_vicaria: 1,
      total_catequistas: { $size: "$catequistas" },
      "catequistas.nombre_completo": 1,
      "catequistas.especialidad": 1
    }
  }
]).pretty();

// --- 7.4 BÚSQUEDA DE TEXTO ---
print("\n--- Búsqueda de Texto ---\n");

// Crear índice de texto
print("1. Creando índice de texto...");
db.catequistas.createIndex({ 
  nombre: "text", 
  apellido: "text", 
  notas: "text" 
}, { name: "text_search_index" });

// Buscar por texto
print("2. Buscando 'María':");
db.catequistas.find({
  $text: { $search: "María" }
}).pretty();

// --- 7.5 GEOESPACIAL ---
print("\n--- Consultas Geoespaciales ---\n");

// Crear índice geoespacial
print("1. Creando índice geoespacial...");
db.parroquias.createIndex({ "ubicacion.coordenadas": "2dsphere" });

// Buscar parroquias cercanas a un punto
print("2. Parroquias cerca de un punto:");
db.parroquias.find({
  "ubicacion.coordenadas": {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [-78.4500, -0.2000]
      },
      $maxDistance: 5000  // 5 km
    }
  }
}).pretty();

// =============================================================================
// 8. FUNCIONES ÚTILES Y MANTENIMIENTO
// =============================================================================

print("\n=== PASO 8: FUNCIONES ÚTILES Y MANTENIMIENTO ===\n");

// --- 8.1 ESTADÍSTICAS DE LA BASE DE DATOS ---
print("--- Estadísticas de la Base de Datos ---\n");

print("1. Estadísticas generales:");
db.stats();

print("\n2. Estadísticas de colección (catequizandos):");
db.catequizandos.stats();

// --- 8.2 VALIDAR COLECCIÓN ---
print("\n--- Validar Colección ---\n");

print("1. Validando colección catequizandos:");
db.catequizandos.validate();

// --- 8.3 LISTAR ÍNDICES ---
print("\n--- Listar Índices ---\n");

print("1. Índices de catequistas:");
db.catequistas.getIndexes();

print("\n2. Índices de grupos:");
db.grupos.getIndexes();

// --- 8.4 EXPLICAR CONSULTAS (PERFORMANCE) ---
print("\n--- Explicar Consultas (Performance) ---\n");

print("1. Análisis de consulta:");
db.catequizandos.find({ parroquia_id: "PAR001" }).explain("executionStats");

// --- 8.5 BACKUP Y RESTORE (Comandos de sistema) ---
print("\n--- Backup y Restore ---\n");
print("Comandos para ejecutar en terminal:");
print("Backup:");
print("  mongodump --uri='mongodb://...' --db=CatequesisDB --out=/backup/path");
print("\nRestore:");
print("  mongorestore --uri='mongodb://...' --db=CatequesisDB /backup/path/CatequesisDB");

// --- 8.6 ELIMINAR ÍNDICES ---
print("\n--- Eliminar Índices (si es necesario) ---\n");

// Eliminar un índice específico
// db.catequistas.dropIndex("cedula_1");

// Eliminar todos los índices excepto _id
// db.catequistas.dropIndexes();

print("(Comentado para proteger índices)");

// =============================================================================
// 9. CONSULTAS ESPECÍFICAS DEL SISTEMA DE CATEQUESIS
// =============================================================================

print("\n=== PASO 9: CONSULTAS ESPECÍFICAS DEL SISTEMA ===\n");

// --- 9.1 REPORTES ---
print("--- Reportes ---\n");

// Reporte: Cupos disponibles por grupo
print("1. Reporte de Cupos Disponibles:");
db.grupos.aggregate([
  {
    $match: { activo: true }
  },
  {
    $lookup: {
      from: "parroquias",
      localField: "parroquia_id",
      foreignField: "_id",
      as: "parroquia"
    }
  },
  {
    $unwind: "$parroquia"
  },
  {
    $project: {
      nombre_grupo: 1,
      sacramento: 1,
      horario: 1,
      cupos_disponibles: 1,
      cupo_maximo: 1,
      porcentaje_ocupacion: {
        $multiply: [
          { $divide: [
            { $subtract: ["$cupo_maximo", "$cupos_disponibles"] },
            "$cupo_maximo"
          ]},
          100
        ]
      },
      "parroquia.nombre": 1
    }
  },
  {
    $sort: { cupos_disponibles: -1 }
  }
]).pretty();

// Reporte: Catequistas por especialidad
print("\n2. Reporte de Catequistas por Especialidad:");
db.catequistas.aggregate([
  {
    $match: { activo: true }
  },
  {
    $group: {
      _id: "$especialidad",
      total: { $sum: 1 },
      catequistas: {
        $push: {
          nombre: "$nombre_completo",
          parroquia: "$parroquia_id"
        }
      }
    }
  },
  {
    $sort: { total: -1 }
  }
]).pretty();

// Reporte: Catequizandos próximos a recibir sacramento
print("\n3. Catequizandos por nivel:");
db.catequizandos.aggregate([
  {
    $match: { activo: true }
  },
  {
    $group: {
      _id: "$nivel",
      total: { $sum: 1 },
      edad_promedio: { $avg: "$edad" }
    }
  },
  {
    $sort: { total: -1 }
  }
]).pretty();

// --- 9.2 FUNCIONES PERSONALIZADAS ---
print("\n--- Funciones Personalizadas ---\n");

// Función para inscribir un catequizando
function inscribirCatequizando(datosNuevo) {
  print("Inscribiendo nuevo catequizando...");
  
  // 1. Validar que el grupo tenga cupos
  var grupo = db.grupos.findOne({ 
    _id: datosNuevo.grupo_id,
    activo: true,
    cupos_disponibles: { $gt: 0 }
  });
  
  if (!grupo) {
    print("✗ Error: El grupo no tiene cupos disponibles");
    return false;
  }
  
  // 2. Insertar catequizando
  var datosCompletos = Object.assign({}, datosNuevo, {
    fecha_creacion: new Date(),
    fecha_actualizacion: new Date()
  });
  var resultado = db.catequizandos.insertOne(datosCompletos);
  
  if (!resultado.acknowledged) {
    print("✗ Error al insertar catequizando");
    return false;
  }
  
  // 3. Actualizar cupos del grupo
  db.grupos.updateOne(
    { _id: datosNuevo.grupo_id },
    {
      $inc: { 
        numero_estudiantes: 1,
        cupos_disponibles: -1
      },
      $push: { catequizandos_ids: resultado.insertedId },
      $set: { fecha_actualizacion: new Date() }
    }
  );
  
  print("✓ Catequizando inscrito exitosamente");
  print("ID: " + resultado.insertedId);
  return true;
}

// Función para transferir catequizando a otro grupo
function transferirCatequizando(catequizandoId, nuevoGrupoId) {
  print("Transfiriendo catequizando...");
  
  // 1. Obtener catequizando actual
  var catequizando = db.catequizandos.findOne({ _id: catequizandoId });
  if (!catequizando) {
    print("✗ Error: Catequizando no encontrado");
    return false;
  }
  
  var grupoAnterior = catequizando.grupo_id;
  
  // 2. Validar nuevo grupo
  var nuevoGrupo = db.grupos.findOne({
    _id: nuevoGrupoId,
    activo: true,
    cupos_disponibles: { $gt: 0 }
  });
  
  if (!nuevoGrupo) {
    print("✗ Error: El nuevo grupo no tiene cupos disponibles");
    return false;
  }
  
  // 3. Actualizar catequizando
  db.catequizandos.updateOne(
    { _id: catequizandoId },
    {
      $set: {
        grupo_id: nuevoGrupoId,
        parroquia_id: nuevoGrupo.parroquia_id,
        fecha_actualizacion: new Date()
      }
    }
  );
  
  // 4. Actualizar grupo anterior (liberar cupo)
  db.grupos.updateOne(
    { _id: grupoAnterior },
    {
      $inc: {
        numero_estudiantes: -1,
        cupos_disponibles: 1
      },
      $pull: { catequizandos_ids: catequizandoId },
      $set: { fecha_actualizacion: new Date() }
    }
  );
  
  // 5. Actualizar nuevo grupo (ocupar cupo)
  db.grupos.updateOne(
    { _id: nuevoGrupoId },
    {
      $inc: {
        numero_estudiantes: 1,
        cupos_disponibles: -1
      },
      $push: { catequizandos_ids: catequizandoId },
      $set: { fecha_actualizacion: new Date() }
    }
  );
  
  print("✓ Catequizando transferido exitosamente");
  return true;
}

// Función para generar reporte de asistencia
function reporteAsistenciaParroquia(parroquiaId) {
  print("Generando reporte de asistencia para parroquia " + parroquiaId);
  
  return db.grupos.aggregate([
    {
      $match: { 
        parroquia_id: parroquiaId,
        activo: true 
      }
    },
    {
      $lookup: {
        from: "catequistas",
        localField: "catequista_id",
        foreignField: "_id",
        as: "catequista"
      }
    },
    {
      $unwind: "$catequista"
    },
    {
      $lookup: {
        from: "catequizandos",
        localField: "_id",
        foreignField: "grupo_id",
        as: "estudiantes"
      }
    },
    {
      $project: {
        nombre_grupo: 1,
        sacramento: 1,
        horario: 1,
        aula: 1,
        catequista: "$catequista.nombre_completo",
        total_estudiantes: { $size: "$estudiantes" },
        cupo_maximo: 1,
        porcentaje_ocupacion: {
          $multiply: [
            { $divide: [
              { $size: "$estudiantes" },
              "$cupo_maximo"
            ]},
            100
          ]
        }
      }
    },
    {
      $sort: { nombre_grupo: 1 }
    }
  ]).toArray();
}

print("\n✓ Funciones personalizadas definidas");

// =============================================================================
// 10. EJEMPLO DE USO COMPLETO
// =============================================================================

print("\n=== PASO 10: EJEMPLO DE USO COMPLETO ===\n");

print("--- Flujo Completo de Inscripción ---\n");

// 1. Consultar grupos disponibles
print("1. Grupos disponibles con cupos:");
var gruposDisponibles = db.grupos.find({
  activo: true,
  cupos_disponibles: { $gt: 0 }
}, {
  nombre_grupo: 1,
  sacramento: 1,
  horario: 1,
  cupos_disponibles: 1
}).toArray();

printjson(gruposDisponibles);

// 2. Inscribir un nuevo catequizando (ejemplo comentado)
/*
var nuevoCatequizando = {
  _id: "CZO999",
  nombre: "Nuevo",
  apellido: "Estudiante",
  nombre_completo: "Nuevo Estudiante",
  cedula: "1750999999",
  fecha_nacimiento: new Date("2015-03-15"),
  edad: 10,
  telefono: "0999999999",
  correo: "nuevo@estudiante.ec",
  direccion: "Dirección de ejemplo",
  nombre_padre: "Padre Ejemplo",
  nombre_madre: "Madre Ejemplo",
  telefono_padres: "0999999998",
  padrino: { nombre: "Padrino", telefono: "", parroquia_bautismo: "PAR001" },
  madrina: { nombre: "Madrina", telefono: "", parroquia_bautismo: "PAR001" },
  parroquia_id: "PAR001",
  grupo_id: "GRP2024A",
  nivel: "Primera Comunión - Nivel 2",
  certificados: [],
  sacramentos_recibidos: ["Bautismo"],
  fecha_inscripcion: new Date(),
  observaciones_medicas: "",
  activo: true,
  notas: ""
};

inscribirCatequizando(nuevoCatequizando);
*/

// 3. Generar reporte
print("\n2. Reporte de asistencia PAR001:");
var reporte = reporteAsistenciaParroquia("PAR001");
printjson(reporte);

// =============================================================================
// RESUMEN FINAL
// =============================================================================

print("\n=============================================================================");
print("  RESUMEN DE OPERACIONES CRUD EN MONGODB");
print("=============================================================================\n");

print("✓ CREATE (Insertar):");
print("  - insertOne()    : Insertar un documento");
print("  - insertMany()   : Insertar múltiples documentos");

print("\n✓ READ (Consultar):");
print("  - find()         : Buscar documentos");
print("  - findOne()      : Buscar un documento");
print("  - aggregate()    : Agregaciones y análisis");
print("  - count()        : Contar documentos");

print("\n✓ UPDATE (Actualizar):");
print("  - updateOne()    : Actualizar un documento");
print("  - updateMany()   : Actualizar múltiples documentos");
print("  - replaceOne()   : Reemplazar un documento completo");
print("  - findAndModify(): Buscar y modificar en una operación");

print("\n✓ DELETE (Eliminar):");
print("  - deleteOne()    : Eliminar un documento");
print("  - deleteMany()   : Eliminar múltiples documentos");
print("  - findAndRemove(): Buscar y eliminar en una operación");

print("\n✓ OPERADORES PRINCIPALES:");
print("  Comparación: $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin");
print("  Lógicos: $and, $or, $not, $nor");
print("  Actualización: $set, $unset, $inc, $push, $pull, $addToSet");
print("  Arrays: $all, $elemMatch, $size");
print("  Proyección: $project, $slice, $elemMatch");

print("\n=============================================================================");
print("  Sistema de Gestión de Catequesis - Operaciones completadas exitosamente");
print("=============================================================================\n");

print("Para más información, visita:");
print("- MongoDB Documentation: https://docs.mongodb.com");
print("- Video Tutorial: https://www.youtube.com/watch?v=WUok6mcBhjI");
print("\n¡Gracias por usar el Sistema de Gestión de Catequesis!\n");
