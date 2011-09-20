<?php session_start();
	function __autoload($class_name) { include_once strtolower($class_name) . '.php'; }
?>

<script type="text/javascript">
	$(document).ready( function () {
		$("#person_course_wrapper").hide();
		$(".search_person").click(function(e) {
			e.preventDefault();
			
			$("#search_wrapper").hide();
			
			$.get("includes/person_course_view.php", { "rcsid": $(this).attr("id") }, function (data) {
				$("#person_course_wrapper").html(data);
			});
			$("#person_course_wrapper").show();	
		});
		
		$(".search_course").click(function(e) {
			e.preventDefault();
			
			$("#search_wrapper").hide();
			
			$.get("includes/person_course_view.php", { "id": $(this).attr("id") }, function (data) {
				$("#person_course_wrapper").html(data);
			});
			$("#person_course_wrapper").show();	
		});
	});
</script>

<div id="search_wrapper">
<?php 
	$search_person = $_SESSION["person"];
	$search_term = $_GET["term"];
	$found_people = $search_person->search( $search_term );
	
	$search_course = new Course();
	$found_course = $search_course->search( $search_term );
	
	echo "<h2>Search Results for \"$search_term\"";
	
	echo "<h4>People</h4>";
	if ($found_people) {
		echo "<ul>";
		foreach ( $found_people as $x ) {
			echo "<li class=\"search_person\" id=\"" . $x->get_id() ."\">";
			echo "<img style=\"margin-left: 10px;\" class=\"person_search_image float_left\" />";
			echo "<span style=\"margin-left: 10px;\" class=\"float_left\"><h3 style=\"margin-top: 2px\">" . $x->get_full_name() . "</h3>";
			echo "<h6 style=\"margin-top: 0px\">" . $x->get_major() . " | Class of " . $x->get_year() . "</h6></span>";
			echo "</li>";
		}
		
		echo "</ul>";
	}

	else echo "<p>No people found with the name $search_term.</p>";
	echo "<div class=\"clear\"></div>";
	echo "<h4>Courses</h4>";
	
	if ($found_course) {
		echo "<ul>";
		foreach ( $found_course as $y ) {
			echo "<li class=\"search_course\" id=\"" . $y->get_id() . "\">";
			echo "<h3 style=\"margin-left: 10px;\">". $y->get_name() ."</h3>";
			echo "</li>";
		}
		echo "</ul>";

	}

	else echo "<p>No course found with the name $search_term.</p>";

	echo "<div class=\"clear\"></div>";
?>
</div>

<div id="person_course_wrapper"></div>