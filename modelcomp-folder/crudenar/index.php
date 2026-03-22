<?php include 'header.php'; ?>
<?php include 'sidebar.php'; ?>

<div class="content-wrapper">
    <?php
        $page = $_GET['page'] ?? 'dashboard';

        switch ($page) {
            case 'student':
                include './student/index.php';
                break;

            case 'faculty':
                include './faculty/index.php';
                break;

            default:
                include './dashboard.php'; 
                break;
        }
    ?>
</div>

<?php include 'footer.php'; ?>