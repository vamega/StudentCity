<?php session_start();
function __autoload($class_name) { include_once strtolower($class_name) . '.php'; }

$person = $_SESSION["person"];

$fname = $_POST["first_name"];
$lname = $_POST["last_name"];
$year = $_POST["class_year"];
$major = $_POST["first_major"];

if (isset($_POST["second_major"])) $major2 = $_POST["second_major"];
else $major2 = "";

if (isset($_POST["profile_pic"])) $pic = $_POST["profile_pic"];
else $pic = 0;

if (isset($_POST["current_classes"])) $currclass = $_POST["current_classes"];
else $currclass = 0;

if (isset($_POST["email_messages"])) $email = $_POST["email_messages"];
else $email = 0;

if ($person->profile_update($fname, $lname, $year, $major, $major2, $pic, $currclass, $email)) {
	echo json_encode(array("error"=>"false"));
	$_SESSION["person"] = $person;
}

else echo json_encode(array("error"=>"true", "message"=>$person->error));

?>