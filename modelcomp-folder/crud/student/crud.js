const modalEstudiante = new bootstrap.Modal(document.getElementById('modalEstudiante'));
const formEstudiante = document.getElementById('formEstudiante');

document.addEventListener('DOMContentLoaded', () => {
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
            console.log("FUNCIONA EL SUBMIT");
            
            e.preventDefault();
            const datos = new FormData(formEstudiante);

            try {
                const resp = await fetch('student/connectajax.php', { method: 'POST', body: datos });
                const resultado = await resp.json();
                
                if (resultado.status === 'ok') {
                    location.reload(); // Recargamos para ver cambios o actualizamos el DOM manualmente
                }
            } catch (error) { console.error("Error:", error); }
        });
    } else {
        console.error("No se encontró el formulario 'formEstudiante' o no se pudo cargar el modal en el HTML.")
    }
});

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

    const resp = await fetch('connectajax.php', { method: 'POST', body: datos });
    if (resp.ok) fila.remove();
}