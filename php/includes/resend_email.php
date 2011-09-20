<?php session_start();

if (isset($_GET["id"])) { 
	confirm_email($_GET["id"]); 
	header("Location: ../index.php");
}

function confirm_email($id) {
	$confirm_code = md5($id.$id);
	$email = $id."@rpi.edu";
	$subject = "StudentCity Confirmation";
	
	$link = "<a href=\"http://localhost:80/studentcity/index.php?id=$id&confirm=$confirm_code\">localhost:80/studentcity/index.php?id=$id&confirm=$confirm_code</a>";
	$message = "<h3>Welcome to StudentCity<h3><p>This was sent to you in order to verify your email address as $email. If you did not register for StudentCity, then please disregard this message. If you would like to continue with your registration with StudentCity, please click on the following link (or copy and paste it into your browser).</p><p>$link</p><p>If you are having problems with this confirmation link, please send a message to greenj12@rpi.edu expressing your concerns.</p>";
	
	$headers = "From: StudentCity Admin <greenj12@rpi.edu>\r\nContent-Type: text/html;";
	
	if(mail($email, $subject, $message, $headers)) return $confirm_code;
	else return false;
}
?>