<?php
require_once('db_conn.php');

if (isset($_POST['user_id'])) {

    $user_id = $_POST['user_id'];
    $query = "SELECT fname, lname FROM user_details WHERE id='$user_id'";

    $result = mysqli_query($connection, $query) or die(mysqli_error($connection));
    $count = mysqli_num_rows($result);
    
    if ($count != 0) {
        $row = mysqli_fetch_assoc($result);
        echo "<script type='text/javascript'>alert('$row[fname],$row[lname]')</script>";
    }
    else {
        echo "<script type='text/javascript'>alert('No results!')</script>";
    }

}
?>