<?php session_start();
function __autoload($class_name) { include_once "includes/" . strtolower($class_name) . '.php'; }

if (!isset($_SESSION["person"])) {
	echo "Nothing";
	exit();
}

$person = $_SESSION["person"];

$classes = $person->get_current_courses();
$_SESSION["courses"] = $classes;

$user = $person->get_first_name();
?>

<!DOCTYPE html>

<html>
<head>
	<title>StudentCity | Dashboard</title>
    <link rel="stylesheet" type="text/css" href="css/base.css" />
    
    <script type="text/javascript" src="javascript/jquery.js"></script>
    <script type="text/javascript" src="javascript/validate.js"></script>
	<script type="text/javascript" src="javascript/custom_functions.js"></script>

    <script>
	$( document ).ready( function () {
		
		$( "#date" ).html(makeDate());
		clearOrRestoreSearchBar();
		
		$( ".course_tile" ).click( function () {
			$( ".course_tile" ).css( "background-image", "url(./images/course_tile.png)" );
			$(this).css( "background-image", "url(./images/course_tile_long.png)" );
			
			$.get("includes/course_info.php", { id: $(this).attr("id") }, function (data) {
				$( "#right_side" ).html(data);
			});
		});
		
		$("#submit").click(function(e) { 
			e.preventDefault();
			
			$.get("includes/search.php", { term: $("#main_search").val() }, function (data) {
				openMyModal(data);
			});
		});
		
		$("#settings_link").click(function(e) { 
			e.preventDefault();
			
			$.get("includes/dashboard_settings.php", 0, function (data) {
				openMyModal(data);
			});
		});
		
		$(".search_person").click(function(e) {
			e.preventDefault();
			
			alert($(this).attr("id"));	
		});
	});
	
	function makeDate() {
		var m_names = new Array("January", "February", "March", "April", "May", 
		"June", "July", "August", "September", "October", "November", "December");

		var d = new Date();
		var curr_date = d.getDate();
		var curr_month = d.getMonth();
		var curr_year = d.getFullYear();
		return m_names[curr_month] + " " + curr_date + ", " + curr_year;	
	}
	
	function clearOrRestoreSearchBar() {
		// If the box says "Search site" then clear it.
		$("#main_search").focus(function() {
			if ( $(this).val() == "Search site" ) {
				$(this).attr("value", "");
			}
		});
		
		// If the box has nothing in it when it loses focus, then put in Search sit.
		$("#main_search").focusout(function() {
			if ( $(this).val() == "" ) {
				$(this).attr("value", "Search site");
			}
		});
	}	
	</script>
</head>

<body id="dashboard">    
    <div id="header">
        <div id="logo"></div>
        <div id="header_wrapper">
        	<div class="float_left">
        		<h3>Welcome <?= $user; ?>!</h3>
                <h3 id="date"></h3>
            </div>
            
            <div class="float_right">
            	<h3 style="text-align: right"><a href="" id="settings_link">Settings</a> | <a href="index.php?logout=1" id="logout">Logout</a></h3>
                <form id="site_search">
            		<input id="submit" class="search_submit" type="submit" value="" />
            		<input id="main_search" type="text" value="Search site" />
        		</form>
            </div>
     	</div>
    </div>
	<div id="wrapper" class="index">
    	<div id="left_side" class="float_left">
        	<?php 
				if (isset($classes)) {
					foreach( $classes as $x ) {
						echo "<div class=\"course_tile\" id=" . $x->get_id() . ">";
						echo 	"<div class=\"text\">";
						echo 		"<h2>" . $x->get_name() . "</h2>";
						echo 		"<h6>Currents ".$x->get_numcurrpeople().": | Veterans: ".$x->get_numpastpeople()."</h6>";
						echo 	"</div>";
						echo "</div>";
					}
				}
			?>
        </div>
        
        <div id="right_side" class="float_right">
        	<h1>Welcome to Student City!</h1>
            <p>
            If you already have classes, click on one to the left to get started. If you don't have any classes, why are you at school!? Go home! Or, you can just add some by entering in the name of your class in the search bar and adding it from there.
            </p>
    </div>
    
    <div class="clear"></div>
    <div id="footer"></div>
</body>
</html>