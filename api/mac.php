<?php

$con = mysqli_connect("127.0.0.1", "eleitin_amazon", "Amazon@123", "eleitin_amazon") or die("No Database Connection");

$mac = $_POST["mac"];
 
$select_mac = " SELECT * FROM `mac_address` WHERE mac = '$mac' AND status='1' ";
$query = mysqli_query($con, $select_mac) or die("mac address not insert");

if(mysqli_num_rows($query) > 0){
	echo "true";
}else{
	echo "false";
}

?>