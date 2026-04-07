<?php
    require_once './connectdb.php';
    header('Content-Type: application/json');

    $accion = $_POST['accion'] ?? '';
    $response = ['status' => 'error'];

    try {
        if ($accion === 'crear') {
            $sql = "INSERT INTO student (code, first_name, last_name, email, faculty) VALUES (?, ?, ?, ?, ?)";
            $stmt = $myPDO->prepare($sql);
            $stmt->execute([$_POST['code'], $_POST['first_name'], $_POST['last_name'], $_POST['email'], $_POST['faculty'] ?? '']);
            $response['status'] = 'ok';
        } 

        elseif ($accion === 'editar') {
            $sql = "UPDATE student SET first_name=?, last_name=?, email=?, faculty=? WHERE code=?";
            $stmt = $myPDO->prepare($sql);
            $stmt->execute([$_POST['first_name'], $_POST['last_name'], $_POST['email'], $_POST['faculty'], $_POST['code']]);
            $response['status'] = 'ok';
        }

        elseif ($accion === 'eliminar') {
            $stmt = $myPDO->prepare("DELETE FROM student WHERE code = ?");
            $stmt->execute([$_POST['code']]);
            $response['status'] = 'ok';
        }
    } catch (Exception $e) {
        $response['error'] = $e->getMessage();
    }

    echo json_encode($response);
?>