let modalEstudiante, formEstudiante;

document.addEventListener('DOMContentLoaded', () => {
    // BUSCAR
    const btnBuscar = document.getElementById('btnBuscar');
    const inputBuscar = document.getElementById('inputBuscar');
    
    if(btnBuscar && inputBuscar) {
        btnBuscar.addEventListener('click', realizarBusqueda);
        inputBuscar.addEventListener('keyup', (e) => {
            if (e.key === "Enter") inputBuscar.blur();
            realizarBusqueda(); 
        });
    }
    
    modalEstudiante = new bootstrap.Modal(document.getElementById('modalEstudiante'));
    formEstudiante = document.getElementById('formEstudiante');
    
    if(modalEstudiante && formEstudiante) {
        // ABRIR PARA AGREGAR
        document.getElementById('btnAgregar').addEventListener('click', () => {
            formEstudiante.reset();
            document.getElementById('modalTitulo').innerText = "Nuevo Estudiante";
            document.getElementById('inputAccion').value = "crear";
            document.getElementById('formCode').readOnly = false;
            modalEstudiante.show();
        });

        // ESCUCHAR CLICS EN LA TABLA (Editar y Eliminar)
        document.getElementById('tablaCuerpo').addEventListener('click', (e) => {
            const btn = e.target.closest('button');
            
            if (!btn) return;

            const accion = btn.getAttribute('data-accion');
            const id = btn.getAttribute('data-id');
            const fila = btn.closest('tr');

            if (accion === 'editar') {
                prepararEdicion(id, fila);
            } else if (accion === 'eliminar') {
                prepararEliminacion(id, fila);
            }
        });

        // ENVÍO DE DATOS (CREATE / UPDATE)

        formEstudiante.addEventListener('submit', async (e) => {
            e.preventDefault();
            e.stopImmediatePropagation();
            
            const datos = new FormData(formEstudiante);
            console.log("Query lanzada!");


            try {
                const resp = await fetch('./student/connectajax.php', { method: 'POST', body: datos });
                const resultado = await resp.json();
                
                if (resultado.status != 'ok') {
                    throw new Error("Error resp estudiante");
                }

                location.reload();
            } catch (error) { console.error("Error estudiante:", error); }
        });
    } else {
        console.error("No se encontró el formulario 'formEstudiante' o no se pudo cargar el modal en el HTML.")
    }
});

// FUNCIÓN BUSCAR
function realizarBusqueda() {
    const tablaCuerpo = document.getElementById('tablaCuerpo');
    const inputBuscar = document.getElementById('inputBuscar');
    
    if (!tablaCuerpo || !inputBuscar) return;

    const termino = inputBuscar.value.toLowerCase();
    const filas = tablaCuerpo.getElementsByTagName('tr');

    let coincidencias = 0;

    for (let i = 0; i < filas.length; i++) {
        // Ignorar la fila de "No se encontraron registros" si existe
        if (filas[i].cells.length < 2) continue; 

        // Unimos el texto de todas las celdas de la fila para buscar en cualquier columna
        const textoFila = filas[i].innerText.toLowerCase();

        if (textoFila.includes(termino)) {
            filas[i].style.display = ""; // Mostrar
            coincidencias++;
        } else {
            filas[i].style.display = "none"; // Ocultar
        }
    }
}

// FUNCIÓN EDITAR (Carga datos en el modal)
function prepararEdicion(id, fila) {
    console.log(id, fila);

    document.getElementById('modalTitulo').innerText = "Editar Estudiante";
    document.getElementById('inputAccion').value = "editar";
    document.getElementById('formCode').value = id;
    document.getElementById('formCode').readOnly = true;
    
    // Sacamos los datos directamente de las celdas de la tabla
    document.getElementById('formFirstName').value = fila.cells[1].innerText;
    document.getElementById('formLastName').value = fila.cells[2].innerText;
    document.getElementById('formEmail').value = fila.cells[3].innerText;
    
    modalEstudiante.show();
}

// FUNCIÓN ELIMINAR
async function prepararEliminacion(id, fila) {
    if (!confirm(`¿Eliminar estudiante ${id}?`)) return;

    const datos = new FormData();
    datos.append('accion', 'eliminar');
    datos.append('code', id);

    const resp = await fetch('./student/connectajax.php', { method: 'POST', body: datos });
    if (resp.ok) {
        fila.remove();
        location.reload();
    } 
}
