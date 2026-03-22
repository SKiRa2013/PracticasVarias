<?php
// Incluimos la conexión (ajusta la ruta según donde tengas el archivo)
require_once 'student/connectdb.php'; 

try {
    $stmtEst = $myPDO->query("SELECT COUNT(*) FROM student");
    $totalEstudiantes = $stmtEst->fetchColumn();

    $stmtFac = $myPDO->query('SELECT COUNT(*) FROM faculty WHERE fac_code <> "0000"');
    $totalFacultades = $stmtFac->fetchColumn();
} catch (PDOException $e) {
    $totalEstudiantes = "!";
    $totalFacultades = "!";
}
?>

<div class="content-header">
    <div class="container-fluid">
        <h1 class="m-0">Tablero Principal</h1>
    </div>
</div>

<section class="content">
    <div class="container-fluid">
        <div class="row">
            <div class="col-lg-3 col-6">
                <div class="small-box bg-info">
                    <div class="inner">
                        <h3><?php echo $totalEstudiantes ?> </h3><p>Estudiantes</p>
                    </div>
                    <div class="icon"><i class="fas fa-user-graduate"></i></div>
                    <a href="index.php?page=student" class="small-box-footer">Ver todos <i class="fas fa-arrow-circle-right"></i></a>
                </div>
                <div class="small-box bg-info">
                    <div class="inner">
                        <h3><?php echo $totalFacultades ?> </h3><p>Facultades</p>
                    </div>
                    <div class="icon"><i class="fas fa-building-columns"></i></div>
                    <a href="index.php?page=faculty" class="small-box-footer">Ver todos <i class="fas fa-arrow-circle-right"></i></a>
                </div>
            </div>
            </div>
    </div>
</section>
