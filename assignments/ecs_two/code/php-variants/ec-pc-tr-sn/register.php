<?php  
require('db_conn.php');

if (isset($_POST['user_name']) and isset($_POST['user_pass']) and isset($_POST['first_name'])){
	
    $uname = mysqli_real_escape_string($connection, $_POST['user_name']);
    $upass = mysqli_real_escape_string($connection, $_POST['user_pass']);
    $fname = mysqli_real_escape_string($connection, $_POST['first_name']);
    $lname = mysqli_real_escape_string($connection, $_POST['last_name']);

    $upass = password_hash($upass, PASSWORD_DEFAULT);

    $stmt = $connection->prepare("INSERT INTO user_creds_vtwo (fname,lname,username,password) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("ssss", $fname, $lname, $uname, $upass);

    try {
        $stmt->execute();
    }
    catch(PDOException $e) {
        echo "Error: " . $e->getMessage();
        header("Location: ./login.html");
    }

    $stmt->close();
    $connection->close();

} 
else {
	echo "<script type='text/javascript'>alert('Enter values for all required fields.')</script>";
}

?>