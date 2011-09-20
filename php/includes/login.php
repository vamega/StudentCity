<?php session_start();
require_once("person.php");

$id = $_POST["rcsid"];
$pass = $_POST["password"];

$new_person = new Person($id);
if($new_person->login($id, $pass)) {
	$_SESSION["person"] = $new_person;
	echo json_encode(array("error"=>"false"));
}
else {
	echo json_encode(array("error"=>"true","message"=>$new_person->error));
}
?>
