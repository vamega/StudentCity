<?php session_start();
function __autoload($class_name) { include_once strtolower($class_name) . '.php'; }

$update_person = $_SESSION["person"];
?>

<script type="text/javascript">
$(document).ready( function() {
// Validation for Settings
			$("#settings").validate({
				rules: {	
					first_name: { required: true },
					last_name: { required: true },
					first_major: { required: true },
					class_year: { 
						required: true,
					}
				},
				
				messages: {
					first_name: { required: "First name is required." },
					last_name: { required: "Last name is required." },
					first_major: { required: "At least your first names major is required." },
					class_year: { required: "Your class year is required." }
				},
				
				errorLabelContainer: "#innerErrorMessageBox",
				wrapper: "li",
				submitHandler: function() { 
					var post_data = $("#settings").serialize();
					$.post("includes/update_settings.php", post_data, function(data) {
						$("#rightErrorMessageBoxServer").css("display", "none");
						if (data.error == "true") {
							$("#innerErrorMessageBoxServer").css("display", "block");
							$("#innerErrorMessageBoxServer").html("<label class='error'>" + data.message + "</label>");
							$("#innerErrorMessageBoxServer").removeClass( "successMessageBox" );
							$("#innerErrorMessageBoxServer").addClass( "errorMessageBox" );

						}
						else {
							$("#innerErrorMessageBoxServer").css("display", "block");
							$("#innerErrorMessageBoxServer").html("<label class='success'>" + "Successfully Updated" + "</label>")
							$("#innerErrorMessageBoxServer .label").removeClass( "errorMessageBox" );
							$("#innerErrorMessageBoxServer").addClass( "successMessageBox" );
						}
					},
					"json");
				}
			});	
});
</script>

<h2>Settings</h2>
<div id="innerErrorMessageBox" class="errorMessageBox"></div>
<div id="innerErrorMessageBoxServer" class="errorMessageBox"></div>
<form id="settings" method="post">
	<h4>Personal Settings</h4>
    <div id="settings_name" class="row" style="height: 25px;">
    	<div class="float_left">
            <label>First Name</label>
            <input type="text" name="first_name" value="<?= $update_person->get_first_name(); ?>"/>
        </div>
        
        <div class="float_left" style="margin-left: 22px;">
            <label>Last Name</label>
            <input type="text" name="last_name" value="<?= $update_person->get_last_name(); ?>"/>
        </div>
    </div>
    <div class="clear"></div>
    <div class="row">
        <label>First Major</label>
        <input type="text" name="first_major" value="<?= $update_person->get_major(); ?>"/>
    </div>
    <div class="row">
        <label>Second Major</label>
        <input type="text" name="second_major" value="<?= $update_person->get_major2(); ?>"/>
    </div>
    <div class="row">
        <label>Class Year</label>
        <input type="text" name="class_year" value="<?= $update_person->get_year(); ?>"/>
    </div>
    
    <h4>Privacy Settings</h4>
    <?php 
		$check = "checked";
	?>
    <div class="row privacy">
    	<input type="checkbox" name="profile_pic" value="1" <?php if($update_person->get_picst()) echo $check; ?>/>
        <label>Allow others to see my profile picture</label>
    </div>
   	<div class="row privacy">
    	<input type="checkbox" name="current_classes" value="1" <?php if($update_person->get_currentclassst()) echo $check; ?>/>
        <label>Allow others to see my list of current classes</label>
    </div>
    <div class="row privacy">
    	<input type="checkbox" name="email_messages" value="1" <?php if($update_person->get_emailst()) echo $check; ?>/>
        <label>Allow others to send me email messages</label>
    </div>
    <input type="submit" class="save-window" value="Save" />
</form>