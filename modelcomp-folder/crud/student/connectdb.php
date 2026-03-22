<?php
    $hostDB = 'localhost';
    $nameDB = 'udenar_db';
    $userDB = 'udenar_admin';
    $pwDB = '123udenar';

    $hostPDO = "mysql:host=$hostDB; dbname=$nameDB";
    $myPDO = new PDO($hostPDO, $userDB, $pwDB);

    $myPDO->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $myQuery = $myPDO -> prepare('SELECT * FROM student JOIN faculty ORDER BY code;');
    $myQuery -> execute();
    $result = $myQuery -> fetchAll();
?>