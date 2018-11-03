<?php
require_once('db_conn.php');

if (isset($_POST['fname']) && isset($_POST['lname'])) {

    $fname = $_POST['fname'];
    $lname = $_POST['lname'];

    $query = "INSERT INTO user_details (fname,lname) VALUES ('$fname','$lname')";

    $result = mysqli_query($connection, $query) or die(mysqli_error($connection));
    $count = mysqli_num_rows($result);
    
    if(!empty($result)) {
        echo "<script type='text/javascript'>alert('Done!')</script>";
        header("Location: ./details.html");
    } else {
        echo "<script type='text/javascript'>alert('Error! Try again.')</script>";
    }

}
?>