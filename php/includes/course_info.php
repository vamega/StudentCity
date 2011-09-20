<?php
session_start();
function __autoload($class_name) { include strtolower($class_name) . '.php'; }

$id = $_GET["id"];

$course_list = $_SESSION["courses"];

foreach ( $course_list as $x ) {
	if ( $x->get_id() == $id ) {
		$course = $x;
		break;
	}
}
?>

<script type="text/javascript">
	$(document).ready( function () {
		$(".person_block").click(function(e) {
			e.preventDefault();
			
			$.get("includes/view_person.php", { "rcsid": $(this).attr("id") }, function (data) {
				openMyModal(data);	
			})
		});
	});
</script>

<?php	
echo "<h1>" . $course->get_name() . "</h1>";
echo "<h3 class=\"bold\">Description:</h3>";
echo "<p>" . $course->get_description() . "</p>";

$count = 0;

echo "<h2 class=\"in_course_title\">People Taking This Course</h2>";
echo "<div class=\"in_course\" id=\"current_course_takers\">";
$current_people = $course->get_currpeople($id, 2011, "spring");

if (isset($current_people)) {
	foreach ( $current_people as $c ){
			$p = new Person($c);
			echo "<div class=\"person_block\" id=\"" . $p->get_id() ."\">";
				 echo "<img class=\"person_image\" />";
				 echo "<h5 class=\"person_name\">" . $p->get_full_name() . "</h5>";
			echo "</div>";
			$count = $count + 1;
			if ($count == 7){
				 echo "<div class=\"clear\"></div>";
				 $count = 0;
			}
	}
}
echo "</div>";

$count = 0;
echo "<h2 class=\"in_course_title\">People Who Completed This Course</h2>";
echo "<div class=\"in_course\" id=\"past_course_takers\"></div>";
$past_people = $course->get_pastpeople();
if (isset( $past_people )) {
	foreach ( $past_people as $c ){
			$p = new Person($c);
			echo "<div class=\"person_block\" id=\"" . $p->get_id() ."\">";
				 echo "<img class=\"person_image\" />";
				 echo "<h5 class=\"person_name\">" . $p->get_full_name() . "</h5>";
			echo "</div>";
			$count = $count + 1;
			if ($count == 7){
				 echo "<div class=\"clear\"></div>";
				 $count = 0;
			}
	}
}
echo "</div>";

?>