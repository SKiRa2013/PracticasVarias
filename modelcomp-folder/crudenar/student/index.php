<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestión de Estudiantes</title>
    <link href="../includes/bootstrap/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="../includes/bootstrap/bootstrap-icons.css">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <div class="card shadow-sm">
            <div class="card-body">
                <div class="row mb-4">
                    <div class="col-md-8">
                        <div class="input-group">
                            <input type="text" class="form-control" placeholder="Buscar estudiante por código o nombre..." id="inputBuscar">
                            <button class="btn btn-primary" type="button" id="btnBuscar">
                                <i class="bi bi-search"></i> </button>
                        </div>
                    </div>
                    <div class="col-md-4 text-end">
                        <button class="btn btn-success w-100" id="btnAgregar">
                            <i class="bi bi-plus-circle me-1"></i> Agregar Estudiante
                        </button>
                    </div>
                </div>

                <div class="row mb-3">
                    <div class="col-12">
                        <div id="contenedorTabla" class="table-responsive">
                            <table class="table table-hover align-middle">
                                <thead class="table-dark">
                                    <tr>
                                        <th>Código</th>
                                        <th>Nombre</th>
                                        <th>Apellido</th>
                                        <th>Email</th>
                                        <th>Facultad</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody id="tablaCuerpo"> 
                                    <?php
                                        ini_set('display_errors', 1);
                                        ini_set('display_startup_errors', 1);
                                        error_reporting(E_ALL);

                                        include './student/connectdb.php';

                                        $isData = false;

                                        foreach($result as $pos => $data){
                                            if(!$isData){
                                                $isData = true;
                                            }
                                        
                                            echo '<tr>
                                                <td>' . $data['code'] . '</td>
                                                <td>' . $data['first_name'] . '</td>
                                                <td>' . $data['last_name'] . '</td>
                                                <td>' . $data['email'] . '</td>
                                                <td>' . $data['fac_name'] . '</td>
                                                <td class="text-center">
                                                    <button class="btn btn-sm btn-outline-primary me-2" title="Editar" 
                                                            data-accion="editar" data-id="' . $data['code'] . '">
                                                        <i class="bi bi-pencil-square"></i>
                                                    </button>

                                                    <button class="btn btn-sm btn-outline-danger" title="Eliminar" 
                                                            data-accion="eliminar" data-id="' . $data['code'] . '">
                                                        <i class="bi bi-trash3"></i>
                                                    </button>
                                                </td>
                                            </tr>';
                                        }

                                        if(!$isData){
                                            echo '<tr>
                                                <td colspan="6" class="text-center text-muted">No se encontraron registros en la base de datos.</td>
                                            </tr>';
                                        }
                                    ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-12 d-flex justify-content-center">
                        <div class="btn-group shadow-sm" role="group" aria-label="Navegación de tabla">
                            <button type="button" class="btn btn-outline-secondary" id="btnPrimero">
                                <i class="bi bi-chevron-double-left"></i> Primero
                            </button>
                            <button type="button" class="btn btn-outline-secondary" id="btnAnterior">
                                <i class="bi bi-chevron-left"></i> Anterior
                            </button>
                            <button type="button" class="btn btn-outline-secondary" id="btnSiguiente">
                                Siguiente <i class="bi bi-chevron-right"></i>
                            </button>
                            <button type="button" class="btn btn-outline-secondary" id="btnUltimo">
                                Último <i class="bi bi-chevron-double-right"></i>
                            </button>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <div class="modal fade" id="modalEstudiante" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <form id="formEstudiante" class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title" id="modalTitulo">Nuevo Estudiante</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <input type="hidden" name="accion" id="inputAccion" value="crear">
                    <div class="mb-3">
                        <label class="form-label">Código</label>
                        <input type="text" name="code" id="formCode" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Nombre</label>
                        <input type="text" name="first_name" id="formFirstName" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Apellido</label>
                        <input type="text" name="last_name" id="formLastName" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" name="email" id="formEmail" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Facultad</label>
                        <select name="faculty" id="formFaculty" class="form-select" required>
                            <option value="0000">-- Seleccione una Facultad --</option>
                            <?php
                                try {
                                    $queryFac = $myPDO->query('SELECT fac_code, fac_name FROM faculty WHERE fac_code <> "0000" ORDER BY fac_code');
                                    while($f = $queryFac->fetch()) {
                                        echo '<option value="' . $f['fac_code'] . '">' . $f['fac_name'] . '</option>';
                                    }
                                } catch (PDOException $e) {
                                    echo '<option value="">Error al cargar facultades</option>';
                                }
                            ?>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="submit" class="btn btn-primary">Guardar Datos</button>
                </div>
            </form>
        </div>
    </div>

    <div class="modal fade" id="modalConfirmarEliminar" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-sm">
            <div class="modal-content">
                <div class="modal-header bg-danger text-white">
                    <h5 class="modal-title">¿Eliminar?</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <p>¿Estás seguro de eliminar al estudiante <br><strong id="labelCodigoEliminar"></strong>?</p>
                </div>
                <div class="modal-footer justify-content-center">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
                    <button type="button" class="btn btn-danger" id="btnConfirmarBorrado">Sí, eliminar</button>
                </div>
            </div>
        </div>
    </div>

    <script src="./includes/bootstrap/js/bootstrap.bundle.min.js"></script>
    <script src="./student/crud.js"></script>
</body>
</html>