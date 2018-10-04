<?php  
require_once('db_conn.php');

if (isset($_POST['user_name']) and isset($_POST['user_pass'])){
	
    $name = $_POST['user_name'];
    $pass = $_POST['user_pass'];
    
    $query = "SELECT * FROM `user_creds` WHERE username='$name' and password='$pass'";
    
    $result = mysqli_query($connection, $query) or die(mysqli_error($connection));
    $count = mysqli_num_rows($result);
    
    if ($count == 1){
        echo "<script type='text/javascript'>alert('Welcome!')</script>";
        header("Location: /landing.html");
        exit;
    } else {
        echo "<script type='text/javascript'>alert('Error!')</script>";
    }
}
?>