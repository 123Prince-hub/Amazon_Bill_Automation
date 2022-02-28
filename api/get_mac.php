<?php

$con = mysqli_connect("127.0.0.1", "eleitin_amazon", "Amazon@123", "eleitin_amazon") or die("No Database Connection");

$response = array();
header('Content-Type: application/json');

$mac = $_POST["mac"];
$name = $_POST["name"];
 
$insert_mac = " INSERT INTO `mac_address`(`mac`, `client_name`) VALUES ('$mac','$name') ";
$query = mysqli_query($con, $insert_mac);

if($query){
	echo "true";
}else{
	echo "false";
}

?>
