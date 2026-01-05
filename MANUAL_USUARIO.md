# 📘 Manual de Usuario - Sistema de Gestión de Catequesis

## 🎯 Introducción

El Sistema de Gestión de Catequesis es una aplicación web que permite administrar de manera integral todos los aspectos relacionados con la catequesis en parroquias: desde el registro de catequizandos hasta la generación de reportes y estadísticas.

---

## 🚀 Cómo Ejecutar el Programa

### Requisitos Previos
- Python 3.8 o superior instalado
- Conexión a Internet (para MongoDB Atlas)

### Paso 1: Instalar Dependencias

Abra una terminal/consola en la carpeta del proyecto y ejecute:

**Windows:**
```cmd
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

### Paso 2: Iniciar el Servidor

**Windows:**
```cmd
cd Backend
python app_catequesis.py
```

**macOS/Linux:**
```bash
cd Backend
python3 app_catequesis.py
```

### Paso 3: Acceder a la Aplicación

1. Espere a ver el mensaje: **"Running on http://127.0.0.1:5001"**
2. Abra su navegador web (Chrome, Firefox, Safari, Edge)
3. Ingrese a la dirección: **http://localhost:5001**

### Detener el Servidor

Presione **CTRL + C** en la terminal donde está corriendo el servidor.

---

## 📋 Funcionalidades Principales

### 1️⃣ Dashboard (Inicio)

**¿Qué hace?**
Es la página principal del sistema que muestra un resumen completo del estado actual de la catequesis.

**Información que puede ver:**
- **Total de Parroquias:** Cantidad de parroquias registradas en el sistema
- **Total de Catequistas:** Número de catequistas activos
- **Total de Grupos:** Cantidad de grupos de catequesis creados
- **Total de Catequizandos:** Número de estudiantes inscritos

**Acciones que puede realizar:**
- Ver estadísticas actualizadas en tiempo real
- Acceder rápidamente al registro de catequizandos
- Navegar a la gestión de grupos
- Ir directamente a la sección de reportes
- Cambiar a cualquier otra seccitodas las parroquias del sistema. Las parroquias son la base del sistema ya que todos los demás registros dependen de ellas.

**Información que puede ver:**
En la tabla de parroquias se muestra:
- Nombre completo de la parroquia
- Nombre de la vicaría a la que pertenece
- Ciudad/ubicación
- Teléfono de contacto
- Nombre del párroco
- Capacidad total de catequesis (cuántos estudiantes puede atender)

**Acciones que puede realizar:**
1. **Registrar una nueva parroquia**
2. **Ver listado completo** de todas las parroquias
3. **Actualizar** la lista de parroquias
4. **Eliminar** parroquias del sistema

**Cómo registrar una parroquia:**
1. Haga clic en la pestaña **⛪ Parroquias**
2. Complete el formulario con los siguientes datos:
   - **Nombre de la Parroquia** *(obligatorio)*: Ej. "Parroquia San José"
   - **Nombre de la Vicaría** *(obligatorio)*: Ej. "Vicaría Norte"
   - **Dirección**: Dirección completa de la parroquia
   - **Ciudad**: Ciudad donde se encuentra
   - **Teléfono** *(obligatorio)*: Número de contacto
   - **Correo**: Email de contacto (opcional)
   - **Nombre del Párroco**: Nombre del sacerdote a cargo
   - **Capacidad de Catequesis**: Número máximo de estudiantes que puede atender (por defecto 100)
3. Haga clic en **💾 Guardar Parroquia**
4. Verá un mensaje verde confirmando el registro exitoso

**Cómo ver las parroquias:**
- La tabla inferior muestra todas las parroquias registradas con sus datos principales
- Use el botón **🔄 Actualizar Lista** para refrescar los datos después de hacer cambios
- Puede ver toda la información de cada parroquia en la tabla

**Cómo eliminar una parroquia:**
1. Localice la parroquia en la tabla
2. Haga clic en el botón **🗑️** (rojo) en la columna de Acciones
3. Confirme la acción en el mensaje que aparece
4. La parrotoda la información de los catequistas que imparten las clases de catequesis en las diferentes parroquias.

**Información que puede ver:**
En la tabla de catequistas se muestra:
- Nombre completo del catequista
- Número de cédula/identificación
- Teléfono de contacto
- Correo electrónico
- Especialidad (sacramento que imparte)
- Acciones disponibles

**Acciones que puede realizar:**
1. **Registrar** nuevos catequistas
2. **Ver listado** de todos los catequistas registrados
3. **Consultar** datos de contacto y especialidades
4. **Filtrar** catequistas por parroquia (mediante la API)
5. **Actualizar** la lista de catequistas
6. **Eliminar** catequistas del sistema

**Cómo registrar un catequista:**
1. Vaya a la pestaña **👥 Catequistas**
2. Complete el formulario con los siguientes datos:
   - **Nombre** *(obligatorio)*: Nombre del catequista
   - **Apellido** *(obligatorio)*: Apellido del catequista
   - **Cédula**: Número de identificación (opcional pero recomendado)
   - **Edad** *(obligatorio)*: Debe ser mayor de 18 años
   - **Teléfono** *(obligatorio)*: Número de contacto
   - **Correo** *(obligatorio)*: Email del catequista
   - **Parroquia** *(obligatorio)*: Seleccione de la lista desplegable
   - **Especialidad**: Sacramento en el que se especializa
     - Primera Comunión
     - Confirmación
     - Bautismo
   - **Dirección**: Dirección de residencia (opcional)
3. Haga clic en **💾 Guardar Catequista**
4. El sistema mostrará un mensaje confirmando el registro

**Información adicional que se guarda automáticamente:**
- Nombre completo (se crea automáticamente combinando nombre y apellido)
- Fecha de creación del registro
- Estado activo/inactivo
- Grupos asignados (se actualiza cuando se crean grupos)
Permite crear y organizar los grupos de catequesis con toda su información: horarios, cupos, catequista asignado y sacramento que se imparte.

**Información que puede ver:**
En la tabla de grupos se muestra:
- **N° Grupo**: Número identificador del grupo
- **Sacramento**: Qué sacramento se prepara (Primera Comunión, Confirmación, Bautismo)
- **Nivel**: Grado o nivel de catequesis
- **Horario**: Día y hora de las clases
- **Estudiantes**: Cantidad de catequizandos inscritos actualmente
- **Cupos Disponibles**: Espacios que quedan para nuevos estudiantes
- Acciones disponibles

**Acciones que puede realizar:**
1. **Crear** nuevos grupos de catequesis
2. **Ver listado** de todos los grupos organizados
3. **Consultar** disponibilidad de cupos en tiempo real
4. **Verificar** horarios y catequistas asignados
5. **Actualizar** la lista de grupos
6. **Eliminar** grupos cuando sea necesario

**Cómo crear un grupo:**
1. Vaya a **📚 Grupos**
2. Complete el formulario con la siguiente información:
   - **Número de Grupo** *(obligatorio)*: Identificador único (Ej: 101, 102, 201)
   - **Sacramento** *(obligatorio)*: Seleccione uno:
Es la función principal del sistema. Permite inscribir estudiantes (catequizandos) con toda su información personal, familiar y de catequesis. Este módulo es el núcleo del sistema ya que registra a todos los estudiantes que participan en la catequesis.

**Información que puede ver:**
En la tabla de catequizandos se muestra:
- **Nombre Completo**: Nombre y apellido del estudiante
- **Edad**: Edad calculada automáticamente desde la fecha de nacimiento
- **Teléfono**: Número de contacto del estudiante
- **Nivel**: Nivel de catequesis en el que está inscrito
- **Padres**: Nombres del padre y madre
- Acciones disponibles

**Acciones que puede realizar:**
1. **Registrar** nuevos catequizandos con información completa
2. **Ver listado** de todos los estudiantes inscritos
3. **Filtrar** catequizandos por grupo específico
4. **Consultar** información personal y familiar
5. **Verificar** datos de contacto de padres y padrinos
6. **Actualizar** la lista de catequizandos
7. **Eliminar** catequizandos cuando sea necesario
8. **Ver** asignación a grupos y parroquias

**Cómo registrar un catequizando paso a paso:**

1. Vaya a la pestaña **👦 Catequizandos**

2. **Sección: Datos Personales**
   - **Nombre** *(obligatorio)*: Nombre del estudiante
   - **Apellido** *(obligatorio)*: Apellido del estudiante
   - **Cédula**: Número de identificación (si aplica)
   - **Fecha de Nacimiento** *(obligatorio)*: Use el selector de fecha
   - **Teléfono** *(obligatorio)*: Número de contacto del estudiante
   - **Correo** *(obligatorio)*: Email del estudiante
   - **Dirección**: Dirección de residencia completa

3. **Sección: Datos de los Padres**
   - **Nombre del Padre**: Nombre completo del padre
   - **Nombre de la Madre**: Nombre completo de la madre
   - **Teléfono de Padres**: Número de contacto de los padres (muy importante para comunicaciones)

4. **Sección: Datos de Padrinos**
   - **Nombre del Padrino**: Nombre completo del padrino de bautismo
   - **Nombre de la Madrina**: Nombre completo de la madrina de bautismo

5. **Sección: Datos de Catequesis**
   - **Parroquia** *(obligatorio)*: 
     - Seleccione la parroquia donde asistirá
     - Al seleccionar, se cargan automáticamente los grupos disponibles
   - **Grupo** *(obligatorio)*: 
     - Seleccione el grupo al que se inscribirá
     - Solo se muestran grupos de la parroquia seleccionada
     - Puede ver los cupos disponibles de cada grupo
   - **Nivel** *(obligatorio)*: Indique el nivel (Ej: "Nivel 1", "Preparación Primera Comunión")

6. Haga clic en **💾 Registrar Catequizando**

**Información que se calcula/genera automáticamente:**
- **Nombre completo**: Se crea combinando nombre y apellido
- **Edad**: Se calcula a partir de la fecha de nacimiento
- **Fecha de inscripción**: Se registra el día del registro
- **Estado activo**: Todos los catequizandos nuevos quedan activos
- **Actualización de cupos**: El grupo seleccionado actualiza sus cupos disponibles

**Cómo ver y filtrar los catequizandos:**

1. **Ver todos los catequizandos:**
   - La tabla muestra todos los estudiantes registrados en el sistema
   - Incluye información principal: nombre, edad, teléfono, nivel y padres

2. **Filtrar por grudetalladas, reportes organizados y permite realizar búsquedas avanzadas de catequizandos. Es una herramienta esencial para análisis y toma de decisiones.

**Información que puede ver y consultar:**

#### 📊 Estadísticas Generales

**Qué información muestra:**
- **Total de Parroquias**: Número total registrado en el sistema
- **Total de Catequistas**: Cantidad de catequistas en el sistema
- **Catequistas Activos**: Cuántos catequistas están actualmente activos
- **Total de Grupos**: Cantidad de grupos creados
- **Grupos Activos**: Grupos que están funcionando actualmente
- **Total de Catequizandos**: Número de estudiantes inscritos
- **Catequizandos Activos**: Estudiantes que continúan en catequesis

**Cómo usar:**
- Las estadísticas se muestran automáticamente al abrir la sección
- Se actualizan cada vez que accede a esta pestaña
- Proporciona una visión general del estado del sistema

#### 🎓 Reporte por Sacramento

**Qué información muestra:**
Para cada sacramento (Primera Comunión, Confirmación, Bautismo):
- Número de grupos que preparan ese sacramento
- Total de estudiantes preparándose para ese sacramento
- Detalles de cada grupo:
  - Número de grupo
  - Cantidad de estudiantes por grupo
  - Catequista asignado (ID)

**Cómo generar el reporte:**
1. En la sección "Catequizandos por Sacramento"
2. Haga clic en **🔄 Generar Reporte**
3. El sistema mostrará un resumen organizado por sacramento
4. Puede ver cuántos estudiantes se preparan para cada sacramento
5. Útil para planificación y organización de ceremonias

**Ejemplo de información que verá:**
```
🎓 Primera Comunión
   Grupos: 3
   Total Estudiantes: 45

🎓 Confirmación
   Grupos: 2
   Total Estudiantes: 28
```

#### 🔍 Búsqueda Avanzada de Catequizandos

**Qué puede buscar:**
- Catequizandos por nombre (parcial o completo)
- El sistema busca coincidencias en nombres y apellidos

**Información que muestra en resultados:**
- Nombre completo del catequizando
- Edad actual
- Teléfono de contacto
- Nivel en el que está inscrito
- Nombres de padre y madre

**Cómo realizar una búsqueda:**
1. En la sección "Búsqueda Avanzada"
2. Escriba el nombre del catequizando en el campo de texto
   - Puede escribir nombre completo o parcial
   - No distingue mayúsculas de minúsculas
   - Ejemplo: "María", "González", "maría gonzález"
3. Haga clic en **🔍 Buscar**
4. El sistema mostrará todos los catequizandos que coincidan
5. Verá un contador: "Resultados de búsqueda (X)"
6. Cada resultado muestra información completa del estudiante

**Casos de uso de los reportes:**

1. **Planificación de ceremonias:**
   - Use el reporte por sacramento para saber cuántos estudiantes necesitan Primera Comunión
   - Organice fechas de ceremonias según cantidad de estudiantes

2. **Control de grupos:**
   - Verifique cuántos grupos hay por sacramento
   - Identifique si necesita crear más grupos

3. **Búsqueda rápida:**
   - Encuentre rápidamente un estudiante por nombre
   - Útil para consultas de padres o verificación de inscripción

4. **Análisis general:**
   - Use las estadísticas para reportes administrativos
   - Compare activos vs. totales para ver deserción

**Acciones que puede realizar:**
1. **Generar** reportes actualizados en tiempo real
2. **Consultar** estadísticas del sistema completo
3. **Buscar** catequizandos específicos por nombre
4. **Analizar** distribución de estudiantes por sacramento
5. **Verificar** estado general del sistema (activos vs. totales)
6. **Exportar** información visualmente (puede copiar los datos mostrados)

**Ejemplo de uso completo:**
1. Registra: "María González", 10 años, de la Parroquia San José
2. Asigna al Grupo 101 (Primera Comunión - Nivel 1)
3. El sistema:
   - Calcula automáticamente la edad (10 años)
   - Registra la fecha de inscripción
   - Actualiza el contador del Grupo 101: 1 estudiante más, 1 cupo menos
   - Guarda toda la información en la base de datos
4. Puede ver a María en la lista de catequizandos
5. Puede filtrar para ver solo los estudiantes del Grupo 101

**⚠️ Requisitos previos:**
- Debe tener parroquias registradas
- Debe tener grupos creados
- Los grupos deben tener cupos disponiblesstrada antes de crear catequistas.

---

### 4️⃣ Gestión de Grupos

**¿Qué hace?**
Crea y organiza los grupos de catequesis con sus horarios y cupos.

**Cómo crear un grupo:**
1. Vaya a **📚 Grupos**
2. Complete:
   - Número de Grupo *(obligatorio)*
   - Sacramento *(obligatorio)*: Primera Comunión, Confirmación o Bautismo
   - Parroquia *(obligatorio)*
   - Catequista *(obligatorio)*
   - Nivel: Ej. "Nivel 1", "Nivel 2"
   - Horario: Ej. "Sábados 9:00 AM - 11:00 AM"
   - Aula
   - Cupo Máximo (por defecto 30)
   - Año Lectivo: Ej. "2025-2026"
3. Clic en **💾 Guardar Grupo**

**Información automática:**
- El sistema calcula automáticamente los cupos disponibles
- Cuando inscribe catequizandos, el contador se actualiza solo

---

### 5️⃣ Registro de Catequizandos ⭐

**¿Qué hace?**
Función principal del sistema. Permite inscribir estudiantes con toda su información.

**Cómo registrar un catequizando:**

1. Vaya a **👦 Catequizandos**

2. **Datos Personales:**
   - Nombre y Apellido *(obligatorios)*
   - Cédula
   - Fecha de Nacimiento *(obligatorio)*
   - Teléfono y Correo *(obligatorios)*
   - Dirección

3. **Datos de los Padres:**
   - Nombre del Padre
   - Nombre de la Madre
   - Teléfono de Padres

4. **Datos de Padrinos:**
   - Nombre del Padrino
   - Nombre de la Madrina

5. **Datos de Catequesis:**
   - Seleccione la Parroquia *(obligatorio)*
   - Seleccione el Grupo *(obligatorio)* - Los grupos se filtran por parroquia
   - Indique el Nivel *(obligatorio)*

6. Clic en **💾 Registrar Catequizando**

**Cómo ver los catequizandos:**
- La tabla inferior muestra todos los estudiantes registrados
- Use el filtro "Filtrar por Grupo" para ver estudiantes de un grupo específico
- Clic en **🔄 Actualizar Lista** para refrescar

---

### 6️⃣ Reportes y Consultas ⭐

**¿Qué hace?**
Genera estadísticas y permite búsquedas avanzadas.

**Estadísticas Generales:**
- Se muestra automáticamente al abrir la sección
- Incluye totales y contadores de elementos activos

**Reporte por Sacramento:**
1. Haga clic en **🔄 Generar Reporte**
2. Verá los catequizandos agrupados por sacramento
3. Muestra cantidad de grupos y estudiantes por cada sacramento

**Búsqueda de Catequizandos:**
1. En "Búsqueda Avanzada", escriba el nombre del catequizando
2. Haga clic en **🔍 Buscar**
3. El sistema mostrará todos los resultados que coincidan

---

## 💡 Consejos de Uso

### Orden Recomendado para el Primer Uso

1. **Primero:** Registre al menos una Parroquia
2. **Segundo:** Registre Catequistas
3. **Tercero:** Cree Grupos de catequesis
4. **Cuarto:** Inscriba Catequizandos

### Navegación

- Use las pestañas superiores para cambiar entre secciones:
  - 📊 Dashboard
  - ⛪ Parroquias
  - 👥 Catequistas
  - 📚 Grupos
  - 👦 Catequizandos
  - 📈 Reportes

### Mensajes del Sistema

- **Verde:** Operación exitosa
- **Rojo:** Error o advertencia
- Los mensajes se cierran automáticamente después de 3 segundos
- También puede cerrarlos haciendo clic en la **X**

### Confirmaciones

- El sistema pedirá confirmación antes de eliminar cualquier registro
- No se puede deshacer una eliminación

---

## ⚠️ Consideraciones Importantes

1. **Dependencias entre Registros:**
   - No puede crear catequistas sin parroquias
   - No puede crear grupos sin parroquias y catequistas
   - No puede inscribir catequizandos sin grupos

2. **Cupos de Grupos:**
   - El sistema controla automáticamente los cupos disponibles
   - Al inscribir un catequizando, el cupo disminuye automáticamente
   - Al eliminar un catequizando, el cupo aumenta automáticamente

3. **Conexión a Internet:**
   - La aplicación requiere conexión a Internet para funcionar
   - Los datos se guardan en MongoDB Atlas (nube)

4. **Actualización de Datos:**
   - Use los botones **🔄 Actualizar Lista** para ver los cambios más recientes
   - El dashboard se actualiza automáticamente al cambiar de sección

---

## 🔧 Solución de Problemas

### El servidor no inicia

**Problema:** Error al ejecutar `python app_catequesis.py`

**Solución:**
1. Verifique que instaló las dependencias: `pip install -r requirements.txt`
2. Intente con `python3` en lugar de `python`
3. Verifique que Python esté instalado: `python --version`

### Puerto en uso

**Problema:** "Address already in use - Port 5001 is in use"

**Solución:**
1. Detenga el servidor anterior (CTRL + C)
2. Cierre otras aplicaciones que puedan usar el puerto 5001
3. Reinicie el servidor

### No se conecta a MongoDB

**Problema:** "Error: No se pudo conectar al servidor MongoDB"

**Solución:**
1. Verifique su conexión a Internet
2. Contacte al administrador del sistema para verificar las credenciales

### La página no carga

**Problema:** El navegador no muestra la aplicación

**Solución:**
1. Verifique que el servidor esté corriendo (debe ver el mensaje en la terminal)
2. Intente con: `http://127.0.0.1:5001` en lugar de `localhost`
3. Limpie el caché del navegador (CTRL + F5)

---

## 📞 Soporte

Para problemas técnicos o dudas adicionales, contacte al administrador del sistema.

---

**Versión:** 1.0  
**Fecha:** Enero 2026  
**Sistema:** CatequesisDB - Gestión Integral de Catequesis
