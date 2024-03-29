<?php session_start();

require_once("includes/person.php");

if ( isset( $_GET["confirm"] )) {
	if(isset($_GET["id"])) {
		$confirm=$_GET["confirm"];
		$id=$_GET["id"];
		$guy = new Person($id);
		if($guy->check_confirm($id, $confirm)==true) {
			$_SESSION["person"] = $guy;
			header("Location: dashboard.php");
			exit();
		}
		error_log(md5($id.$id));
	}
}

if ( isset( $_GET["logout"] )){
       session_destroy();
}

?>

<!DOCTYPE html>

<html>
<head>
	<title>StudentCity | Your Home for Social Academia</title>
    
    <link rel="stylesheet" type="text/css" href="css/base.css" />
    <script type="text/javascript" src="javascript/jquery.js"></script>
    <script type="text/javascript" src="javascript/validate.js"></script>
    <script type="text/javascript" src="javascript/custom_functions.js"></script>

  	<script type="text/javascript">
		$(document).ready(function() {								
			// Validation for the registration!
			$("#registration").validate({
				rules: {	
					rcsid: { required: true },
					pass1: { required: true },
					pass2: { 
						required: true,
						equalTo: "#pass1" }
				},
				
				messages: {
					rcsid: { required: "The RCSID is required." },
					pass1: { required: "The password is required." },
					pass2: { 
						required: "The second password is required.",
						equalTo: "The two passwords must match."
					}
				},
				
				errorLabelContainer: "#rightErrorMessageBox",
				wrapper: "li",
				submitHandler: function() { 
					var post_data = $("#registration").serialize();
					$.post("includes/register.php", post_data, function(data) {
						$("#rightErrorMessageBoxServer").css("display", "none");
						if (data.error == "true") {
							$("#rightErrorMessageBoxServer").css("display", "block");
							$("#rightErrorMessageBoxServer").html("<label class='error'>" + data.message + "</label>");
						}
						else {
							$.get("includes/settings.php", 
								{ id: data.rcs }, 
								function (data) { openMyModal(data); }
							);
						}
					});
				}
			});
			
			$("#login").validate({
				rules: {	
					rcsid: { required: true },
					password: { required: true }
				},
				
				messages: {
					rcsid: { required: "The RCSID is required." },
					password: { required: "The password is required." }
				},
				
				errorLabelContainer: "#leftErrorMessageBox",
				wrapper: "li",
				submitHandler: function() { 
					var post_data = $("#login").serialize();
					$.post("includes/login.php", post_data, function(data) {
						if(data.error == "true") {
							$("#leftErrorMessageBoxServer").css("display", "block");
							$("#leftErrorMessageBoxServer").html("<label class='error'>" + data.message + "</label>");
						}
						else {
							window.location.href = "dashboard.php";
						}
					}, "json");
				}		
			});
		});
	</script>
</head>

<body>
    <div id="header">
        <div id="logo"></div>
    </div>
	<div id="wrapper" class="index">
    	<div id="slogan"></div>
        
        <div>
        <p class="float_left">With StudentCity, you can connect with your classmates in a whole new way, and actually meet people in the classroom, and get to know them outside the classroom. You never again have to worry about those embarassing time when you forget a name!</p>
            
        <p class="float_right">Form groups, find out who has the same class as you, and also get information from those who took a class in the past. StudentCity connects you to other students from the past and present in order to better prepare you for the future.</p>
        </div>
        
        <div class="float_left main_info">            
            <h1>Existing Users Login</h1>
            <div id="leftErrorMessageBoxServer" class="float_right errorMessageBox"></div>
            <div id="leftErrorMessageBox" class="float_right errorMessageBox"></div>
            <form id="login" method="post" action="index.php">
                <input class="float_right text_input" type="text" name="rcsid" />
                <label class="float_right">RCS ID</label>
                <div class="clear"></div>
                <div class="not-first">
               		<input class="float_right text_input" type="password" name="password" />
                	<label class="float_right">Password</label>
                </div>
                <div class="clear"></div>
                <input class="float_right button_input" type="submit" value="Login" />
            </form>
        </div>
        <div class="float_right main_info">
            <h1>New Users Register Here</h1>
            <div id="rightErrorMessageBoxServer" class="errorMessageBox"></div>
            <div id="rightErrorMessageBox" class="errorMessageBox"></div>
            <form  id="registration" method="post">
              <label class="float_left">RCS ID</label>
              <input class="float_left text_input" type="text" name="rcsid"/>
                <div class="clear"></div>
                <div class="not-first">
                	<label class="float_left">Password</label>
               		<input id="pass1" class="float_left text_input" type="password" name="pass1"/>
                </div>
				<div class="clear"></div>
                <div class="not-first">
                	<label class="float_left">Retype Password</label>
               		<input id="pass2" class="float_left text_input" type="password" name="pass2"/>
                </div>
                <div class="clear"></div>
                <input class="float_right button_input" type="submit" value="Register" />
            </form>
      
        </div>
    </div>
    
</body>
</html>