<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "phish_db";

$connection = mysqli_connect($servername, $username, $password);
if (!$connection){
    die("Error in connecting to database!" . mysqli_error($connection));
}
$select_db = mysqli_select_db($connection, $dbname);
if (!$select_db){
    die("Error in accessing the database!" . mysqli_error($connection));
}

?> 