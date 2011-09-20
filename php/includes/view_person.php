<?php session_start();
function __autoload($class_name) { include_once strtolower($class_name) . '.php'; }
?>

<?php 
if ( isset($_GET["rcsid"]) ) {
	echo "<h3 class=\"float_right\"><a href=\"mailto:" . $_GET["rcsid"] ."@rpi.edu\">Email</a></h3>";

	
	$person_searched = new Person ( $_GET["rcsid"] );

?>
<div class="clear"></div>
<div id="person_search_info" style="margin-top: 10px;">
	<img id="person_search_image" class="float_left" />
    
    <div id="name_info" class="float_left" style="height: 110px;">
    	<h1 style="margin-top: 15px;"><?= $person_searched->get_full_name(); ?></h1>
        <h3><?php echo $person_searched->get_major(); if($person_searched->get_major2() != "") echo $person_searched->get_major2(); ?></h3>
        
        <h3><?= $person_searched->get_year(); ?></h3>
    </div>
    
    <div class="clear"></div>
    
    <div id="person_search_clases">
    	<?php $person_searched->update_current_courses(); ?>
    	<h4><?= $person_searched->get_first_name() ?>'s Courses for Spring 2011</h4>
        <?php 
			$these_courses = $person_searched->get_current_courses();
			
			if (isset($these_courses[0])){
				echo "<ul>";
				foreach ($these_courses as $x) {
					error_log("This course is " . $x->get_display_name());
					echo "<li><h3>" . $x->get_display_name() . "</h3></li>";
				}
				echo "<ul>";
			}
		?>	
    </div>
</div>

<?php } 