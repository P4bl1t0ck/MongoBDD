// ==================== CONFIGURACIÓN ====================
const API_URL = 'http://localhost:5001/api';

// ==================== NAVEGACIÓN ====================
function mostrarSeccion(seccionId) {
    // Ocultar todas las secciones
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Mostrar la sección seleccionada
    document.getElementById(seccionId).classList.add('active');
    
    // Actualizar tabs activos
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Cargar datos según la sección
    if (seccionId === 'dashboard') {
        cargarEstadisticas();
    } else if (seccionId === 'parroquias') {
        cargarParroquias();
    } else if (seccionId === 'catequistas') {
        cargarCatequistas();
        cargarParroquiasSelect();
    } else if (seccionId === 'grupos') {
        cargarGrupos();
        cargarParroquiasSelect();
        cargarCatequistasSelect();
    } else if (seccionId === 'catequizandos') {
        cargarCatequizandos();
        cargarParroquiasSelect();
    } else if (seccionId === 'reportes') {
        cargarEstadisticasDetalladas();
    }
}

// ==================== MODAL ====================
function mostrarModal(mensaje, tipo = 'info') {
    const modal = document.getElementById('modal');
    const modalMensaje = document.getElementById('modalMensaje');
    
    modalMensaje.textContent = mensaje;
    modalMensaje.className = tipo === 'error' ? 'error-message' : 'success-message';
    modal.classList.add('active');
    
    // Auto-cerrar después de 3 segundos
    setTimeout(() => cerrarModal(), 3000);
}

function cerrarModal() {
    document.getElementById('modal').classList.remove('active');
}

// ==================== API HELPERS ====================
async function apiRequest(url, method = 'GET', data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error || 'Error en la operación');
        }
        
        return result;
    } catch (error) {
        console.error('Error:', error);
        mostrarModal('Error: ' + error.message, 'error');
        throw error;
    }
}

// ==================== ESTADÍSTICAS ====================
async function cargarEstadisticas() {
    try {
        const stats = await apiRequest(`${API_URL}/estadisticas`);
        
        document.getElementById('totalParroquias').textContent = stats.data.total_parroquias;
        document.getElementById('totalCatequistas').textContent = stats.data.total_catequistas;
        document.getElementById('totalGrupos').textContent = stats.data.total_grupos;
        document.getElementById('totalCatequizandos').textContent = stats.data.total_catequizandos;
    } catch (error) {
        console.error('Error al cargar estadísticas:', error);
    }
}

async function cargarEstadisticasDetalladas() {
    try {
        const stats = await apiRequest(`${API_URL}/estadisticas`);
        const container = document.getElementById('estadisticasDetalladas');
        
        container.innerHTML = `
            <p>📊 Total Parroquias: ${stats.data.total_parroquias}</p>
            <p>👥 Total Catequistas: ${stats.data.total_catequistas}</p>
            <p>✅ Catequistas Activos: ${stats.data.catequistas_activos}</p>
            <p>📚 Total Grupos: ${stats.data.total_grupos}</p>
            <p>✅ Grupos Activos: ${stats.data.grupos_activos}</p>
            <p>👦 Total Catequizandos: ${stats.data.total_catequizandos}</p>
            <p>✅ Catequizandos Activos: ${stats.data.catequizandos_activos}</p>
        `;
    } catch (error) {
        console.error('Error al cargar estadísticas detalladas:', error);
    }
}

// ==================== PARROQUIAS ====================
async function cargarParroquias() {
    try {
        const result = await apiRequest(`${API_URL}/parroquias`);
        const tbody = document.getElementById('cuerpoTablaParroquias');
        
        if (result.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="loading">No hay parroquias registradas</td></tr>';
            return;
        }
        
        tbody.innerHTML = result.data.map(p => `
            <tr>
                <td>${p.nombre}</td>
                <td>${p.nombre_vicaria}</td>
                <td>${p.ubicacion?.ciudad || '-'}</td>
                <td>${p.telefono}</td>
                <td>${p.parroco || '-'}</td>
                <td>${p.capacidad_catequesis}</td>
                <td>
                    <button class="btn btn-danger" onclick="eliminarParroquia('${p._id}')">🗑️</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error al cargar parroquias:', error);
    }
}

async function cargarParroquiasSelect() {
    try {
        const result = await apiRequest(`${API_URL}/parroquias`);
        
        const selects = [
            'catequistaParroquia',
            'grupoParroquia',
            'catequizandoParroquia'
        ];
        
        selects.forEach(selectId => {
            const select = document.getElementById(selectId);
            if (select) {
                select.innerHTML = '<option value="">Seleccionar parroquia...</option>' +
                    result.data.map(p => `<option value="${p._id}">${p.nombre}</option>`).join('');
            }
        });
    } catch (error) {
        console.error('Error al cargar parroquias en select:', error);
    }
}

async function eliminarParroquia(id) {
    if (!confirm('¿Está seguro de eliminar esta parroquia?')) return;
    
    try {
        await apiRequest(`${API_URL}/parroquias/${id}`, 'DELETE');
        mostrarModal('Parroquia eliminada exitosamente');
        cargarParroquias();
    } catch (error) {
        console.error('Error al eliminar parroquia:', error);
    }
}

// ==================== CATEQUISTAS ====================
async function cargarCatequistas() {
    try {
        const result = await apiRequest(`${API_URL}/catequistas`);
        const tbody = document.getElementById('cuerpoCatequistas');
        
        if (result.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="loading">No hay catequistas registrados</td></tr>';
            return;
        }
        
        tbody.innerHTML = result.data.map(c => `
            <tr>
                <td>${c.nombre_completo}</td>
                <td>${c.cedula || '-'}</td>
                <td>${c.telefono}</td>
                <td>${c.correo}</td>
                <td>${c.especialidad || '-'}</td>
                <td>
                    <button class="btn btn-danger" onclick="eliminarCatequista('${c._id}')">🗑️</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error al cargar catequistas:', error);
    }
}

async function cargarCatequistasSelect() {
    try {
        const result = await apiRequest(`${API_URL}/catequistas`);
        const select = document.getElementById('grupoCatequista');
        
        if (select) {
            select.innerHTML = '<option value="">Seleccionar catequista...</option>' +
                result.data.map(c => `<option value="${c._id}">${c.nombre_completo}</option>`).join('');
        }
    } catch (error) {
        console.error('Error al cargar catequistas en select:', error);
    }
}

async function eliminarCatequista(id) {
    if (!confirm('¿Está seguro de eliminar este catequista?')) return;
    
    try {
        await apiRequest(`${API_URL}/catequistas/${id}`, 'DELETE');
        mostrarModal('Catequista eliminado exitosamente');
        cargarCatequistas();
    } catch (error) {
        console.error('Error al eliminar catequista:', error);
    }
}

// ==================== GRUPOS ====================
async function cargarGrupos() {
    try {
        const result = await apiRequest(`${API_URL}/grupos`);
        const tbody = document.getElementById('cuerpoGrupos');
        
        if (result.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="loading">No hay grupos registrados</td></tr>';
            return;
        }
        
        tbody.innerHTML = result.data.map(g => `
            <tr>
                <td>${g.numero_grupo}</td>
                <td>${g.sacramento}</td>
                <td>${g.nivel || '-'}</td>
                <td>${g.horario || '-'}</td>
                <td>${g.numero_estudiantes}</td>
                <td>${g.cupos_disponibles}</td>
                <td>
                    <button class="btn btn-danger" onclick="eliminarGrupo('${g._id}')">🗑️</button>
                </td>
            </tr>
        `).join('');
        
        // Actualizar select de filtro
        const filtroGrupo = document.getElementById('filtroGrupo');
        if (filtroGrupo) {
            filtroGrupo.innerHTML = '<option value="">Todos los grupos</option>' +
                result.data.map(g => `<option value="${g._id}">Grupo ${g.numero_grupo} - ${g.sacramento}</option>`).join('');
        }
    } catch (error) {
        console.error('Error al cargar grupos:', error);
    }
}

async function cargarGruposPorParroquia(parroquiaId, selectId) {
    if (!parroquiaId) {
        document.getElementById(selectId).innerHTML = '<option value="">Primero seleccione parroquia...</option>';
        return;
    }
    
    try {
        const result = await apiRequest(`${API_URL}/grupos?parroquia_id=${parroquiaId}`);
        const select = document.getElementById(selectId);
        
        if (result.data.length === 0) {
            select.innerHTML = '<option value="">No hay grupos en esta parroquia</option>';
            return;
        }
        
        select.innerHTML = '<option value="">Seleccionar grupo...</option>' +
            result.data.map(g => `<option value="${g._id}">Grupo ${g.numero_grupo} - ${g.sacramento} (${g.cupos_disponibles} cupos)</option>`).join('');
    } catch (error) {
        console.error('Error al cargar grupos por parroquia:', error);
    }
}

async function eliminarGrupo(id) {
    if (!confirm('¿Está seguro de eliminar este grupo?')) return;
    
    try {
        await apiRequest(`${API_URL}/grupos/${id}`, 'DELETE');
        mostrarModal('Grupo eliminado exitosamente');
        cargarGrupos();
    } catch (error) {
        console.error('Error al eliminar grupo:', error);
    }
}

// ==================== CATEQUIZANDOS ====================
async function cargarCatequizandos() {
    try {
        const result = await apiRequest(`${API_URL}/catequizandos`);
        const tbody = document.getElementById('cuerpoCatequizandos');
        
        if (result.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="loading">No hay catequizandos registrados</td></tr>';
            return;
        }
        
        tbody.innerHTML = result.data.map(c => `
            <tr>
                <td>${c.nombre_completo}</td>
                <td>${c.edad} años</td>
                <td>${c.telefono}</td>
                <td>${c.nivel}</td>
                <td>${c.nombre_padre || '-'} / ${c.nombre_madre || '-'}</td>
                <td>
                    <button class="btn btn-danger" onclick="eliminarCatequizando('${c._id}')">🗑️</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error al cargar catequizandos:', error);
    }
}

async function filtrarCatequizandos() {
    const grupoId = document.getElementById('filtroGrupo').value;
    
    try {
        const url = grupoId ? `${API_URL}/catequizandos?grupo_id=${grupoId}` : `${API_URL}/catequizandos`;
        const result = await apiRequest(url);
        const tbody = document.getElementById('cuerpoCatequizandos');
        
        if (result.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="loading">No hay catequizandos en este grupo</td></tr>';
            return;
        }
        
        tbody.innerHTML = result.data.map(c => `
            <tr>
                <td>${c.nombre_completo}</td>
                <td>${c.edad} años</td>
                <td>${c.telefono}</td>
                <td>${c.nivel}</td>
                <td>${c.nombre_padre || '-'} / ${c.nombre_madre || '-'}</td>
                <td>
                    <button class="btn btn-danger" onclick="eliminarCatequizando('${c._id}')">🗑️</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error al filtrar catequizandos:', error);
    }
}

async function eliminarCatequizando(id) {
    if (!confirm('¿Está seguro de eliminar este catequizando?')) return;
    
    try {
        await apiRequest(`${API_URL}/catequizandos/${id}`, 'DELETE');
        mostrarModal('Catequizando eliminado exitosamente');
        cargarCatequizandos();
    } catch (error) {
        console.error('Error al eliminar catequizando:', error);
    }
}

// ==================== REPORTES ====================
async function cargarReporteSacramentos() {
    try {
        const result = await apiRequest(`${API_URL}/reportes/por-sacramento`);
        const container = document.getElementById('reporteSacramentos');
        
        if (Object.keys(result.data).length === 0) {
            container.innerHTML = '<p>No hay datos disponibles</p>';
            return;
        }
        
        container.innerHTML = Object.entries(result.data).map(([sacramento, info]) => `
            <div class="report-item">
                <h4>🎓 ${sacramento}</h4>
                <p><strong>Grupos:</strong> ${info.grupos}</p>
                <p><strong>Total Estudiantes:</strong> ${info.estudiantes}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error al cargar reporte de sacramentos:', error);
    }
}

async function buscarCatequizando() {
    const nombre = document.getElementById('buscarNombre').value.trim().toLowerCase();
    
    if (!nombre) {
        mostrarModal('Por favor ingrese un nombre para buscar', 'error');
        return;
    }
    
    try {
        const result = await apiRequest(`${API_URL}/catequizandos`);
        const resultados = result.data.filter(c => 
            c.nombre_completo.toLowerCase().includes(nombre)
        );
        
        const container = document.getElementById('resultadoBusqueda');
        
        if (resultados.length === 0) {
            container.innerHTML = '<p class="error-message">No se encontraron catequizandos con ese nombre</p>';
            return;
        }
        
        container.innerHTML = `
            <h4>Resultados de búsqueda (${resultados.length}):</h4>
            ${resultados.map(c => `
                <div class="report-item">
                    <h4>${c.nombre_completo}</h4>
                    <p><strong>Edad:</strong> ${c.edad} años</p>
                    <p><strong>Teléfono:</strong> ${c.telefono}</p>
                    <p><strong>Nivel:</strong> ${c.nivel}</p>
                    <p><strong>Padres:</strong> ${c.nombre_padre} / ${c.nombre_madre}</p>
                </div>
            `).join('')}
        `;
    } catch (error) {
        console.error('Error al buscar catequizando:', error);
    }
}

// ==================== FORMULARIOS ====================

// Formulario Parroquias
document.getElementById('formParroquia').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        nombre: document.getElementById('parroquiaNombre').value,
        nombre_vicaria: document.getElementById('parroquiaVicaria').value,
        ubicacion: {
            direccion: document.getElementById('parroquiaDireccion').value,
            ciudad: document.getElementById('parroquiaCiudad').value,
            provincia: ''
        },
        telefono: document.getElementById('parroquiaTelefono').value,
        correo: document.getElementById('parroquiaCorreo').value,
        parroco: document.getElementById('parroquiaParroco').value,
        capacidad_catequesis: parseInt(document.getElementById('parroquiaCapacidad').value)
    };
    
    try {
        await apiRequest(`${API_URL}/parroquias`, 'POST', data);
        mostrarModal('Parroquia registrada exitosamente');
        e.target.reset();
        cargarParroquias();
        cargarParroquiasSelect();
    } catch (error) {
        console.error('Error al crear parroquia:', error);
    }
});

// Formulario Catequistas
document.getElementById('formCatequista').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        nombre: document.getElementById('catequistaNombre').value,
        apellido: document.getElementById('catequistaApellido').value,
        cedula: document.getElementById('catequistaCedula').value,
        edad: parseInt(document.getElementById('catequistaEdad').value),
        telefono: document.getElementById('catequistaTelefono').value,
        correo: document.getElementById('catequistaCorreo').value,
        parroquia_id: document.getElementById('catequistaParroquia').value,
        especialidad: document.getElementById('catequistaEspecialidad').value,
        direccion: document.getElementById('catequistaDireccion').value
    };
    
    try {
        await apiRequest(`${API_URL}/catequistas`, 'POST', data);
        mostrarModal('Catequista registrado exitosamente');
        e.target.reset();
        cargarCatequistas();
    } catch (error) {
        console.error('Error al crear catequista:', error);
    }
});

// Formulario Grupos
document.getElementById('formGrupo').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        numero_grupo: parseInt(document.getElementById('grupoNumero').value),
        sacramento: document.getElementById('grupoSacramento').value,
        parroquia_id: document.getElementById('grupoParroquia').value,
        catequista_id: document.getElementById('grupoCatequista').value,
        nivel: document.getElementById('grupoNivel').value,
        horario: document.getElementById('grupoHorario').value,
        aula: document.getElementById('grupoAula').value,
        cupo_maximo: parseInt(document.getElementById('grupoCupo').value),
        año_lectivo: document.getElementById('grupoAño').value
    };
    
    try {
        await apiRequest(`${API_URL}/grupos`, 'POST', data);
        mostrarModal('Grupo creado exitosamente');
        e.target.reset();
        cargarGrupos();
    } catch (error) {
        console.error('Error al crear grupo:', error);
    }
});

// Formulario Catequizandos
document.getElementById('formCatequizando').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        nombre: document.getElementById('catequizandoNombre').value,
        apellido: document.getElementById('catequizandoApellido').value,
        cedula: document.getElementById('catequizandoCedula').value,
        fecha_nacimiento: document.getElementById('catequizandoFechaNac').value,
        telefono: document.getElementById('catequizandoTelefono').value,
        correo: document.getElementById('catequizandoCorreo').value,
        direccion: document.getElementById('catequizandoDireccion').value,
        nombre_padre: document.getElementById('catequizandoPadre').value,
        nombre_madre: document.getElementById('catequizandoMadre').value,
        telefono_padres: document.getElementById('catequizandoTelPadres').value,
        padrino: {
            nombre: document.getElementById('catequizandoPadrino').value
        },
        madrina: {
            nombre: document.getElementById('catequizandoMadrina').value
        },
        parroquia_id: document.getElementById('catequizandoParroquia').value,
        grupo_id: document.getElementById('catequizandoGrupo').value,
        nivel: document.getElementById('catequizandoNivel').value
    };
    
    try {
        await apiRequest(`${API_URL}/catequizandos`, 'POST', data);
        mostrarModal('Catequizando registrado exitosamente');
        e.target.reset();
        cargarCatequizandos();
        cargarGrupos(); // Actualizar contadores de grupos
    } catch (error) {
        console.error('Error al registrar catequizando:', error);
    }
});

// ==================== INICIALIZACIÓN ====================
document.addEventListener('DOMContentLoaded', () => {
    cargarEstadisticas();
    cargarParroquias();
});
