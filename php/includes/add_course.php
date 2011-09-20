<?php session_start();
function __autoload($class_name) { include_once strtolower($class_name) . '.php'; }

if( isset( $_GET["id"] )) {
	$id = $_GET["id"];
	
	$_SESSION["person"]->add_course($id, 2011, "spring");
}
?>