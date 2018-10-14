<?php  
require('db_conn.php');

if (isset($_POST['user_name']) and isset($_POST['user_pass'])){
	
    $name = mysqli_real_escape_string($connection, $_POST['user_name']);
    $pass = mysqli_real_escape_string($connection, $_POST['user_pass']);
    
    $stmt = $connection->prepare("SELECT username, password FROM user_creds_vtwo WHERE username = ?");
    $stmt->bind_param('s', $name);
    $stmt->execute();
    $stmt->bind_result($username, $password);
    $stmt->store_result();
    
    if ($stmt->num_rows == 1) {
        if ($stmt->fetch()) {
            if (password_verify($pass, $password)) {
                header("Location: ./landing.html");
                exit();
            } else {
                echo "Invalid password. Try again.";
                header("Location: ./login.html");
            }
        }
    } else {
        echo "Invalid username. Try again.";
        header("Location: ./login.html");
    }
    
    $stmt->close(); 
    $connection->close();
    
}
?>