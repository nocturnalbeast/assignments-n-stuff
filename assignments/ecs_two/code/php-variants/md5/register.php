<?php  
require('db_conn.php');

if (isset($_POST['user_name']) and isset($_POST['user_pass']) and isset($_POST['first_name'])){
	
    $uname = $_POST['user_name'];
    $upass = md5($_POST['user_pass']);
    $fname = $_POST['first_name'];
    $lname = $_POST['last_name'];
    
    $query = "INSERT INTO user_creds_md5 (fname,lname,username,password) VALUES ('$fname','$lname','$uname','$upass')";
    
    $result = mysqli_query($connection, $query) or die(mysqli_error($connection));
    if(!empty($result)) {
        echo "<script type='text/javascript'>alert('Successfuly registered!!')</script>";
        header("Location: /url/to/the/other/page");
        exit;
        unset($_POST);
    } else {
        echo "<script type='text/javascript'>alert('Error! Try again.')</script>";
    }
} else {
	echo "<script type='text/javascript'>alert('Enter values for all required fields.')</script>";
}

?>