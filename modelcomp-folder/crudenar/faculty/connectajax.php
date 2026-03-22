<?php
    require_once 'connectdb.php';
    header('Content-Type: application/json');

    $accion = $_POST['accion'] ?? '';
    $response = ['status' => 'error'];

    try {
        if ($accion === 'crear') {
            $sql = "INSERT INTO faculty (fac_code, fac_name) VALUES (?, ?)";
            $stmt = $myPDO->prepare($sql);
            $stmt->execute([$_POST['fac_code'], $_POST['fac_name']]);
            $response['status'] = 'ok';
        } 

        elseif ($accion === 'editar') {
            $sql = "UPDATE faculty SET fac_name=? WHERE fac_code=?";
            $stmt = $myPDO->prepare($sql);
            $stmt->execute([$_POST['fac_name'], $_POST['fac_code']]);
            $response['status'] = 'ok';
        }
        
        elseif ($accion === 'eliminar') {
            $stmt = $myPDO->prepare("UPDATE student SET faculty='0000' WHERE faculty = ?");
            $stmt->execute([$_POST['fac_code']]);
            
            $stmt = $myPDO->prepare("DELETE FROM faculty WHERE fac_code = ?");
            $stmt->execute([$_POST['fac_code']]);

            $response['status'] = 'ok';
        }
    } catch (Exception $e) {
        $response['error'] = $e->getMessage();
    }

    echo json_encode($response);
?>