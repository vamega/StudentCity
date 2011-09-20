<?php
require_once("database_class.php");

class Course
{
	private $id;
	private $department;
	private $number;		//course number, 4 digit number
	private $name;
	private $description;
	private $year;
	private $season;
	private $currentpeople;
	private $numcurrentpeople;
	private $pastpeople;
	private $numpastpeople;
	public $error;
	
	public function search($in_name) {
		$db = new Database();
		$db->connect();
		$sql = "SELECT * FROM courses WHERE concat_ws(' ', department, number) LIKE '%".$in_name."%' OR name LIKE '%".$in_name."%' OR description LIKE '%".$in_name."%' LIMIT 30";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		if(mysql_num_rows($result) == 0) {
			$this->error = "No people results were found for that search term";
			return false;
		}
		while ($row=mysql_fetch_array($result)) {
			$temp = new Course();
			$temp->simpconstruct($row['id']);
			$tcurrcourses[] = $temp;
		}
		
		return $tcurrcourses;
	}
	
	public function get_display_name () {
		return $this->department . " " . $this->number . " - " . $this->name;	
	}
	
	public function full_update_course() {
		if(is_null($this->year) || is_null($this->season)) {
			return $this->simpconstruct($this->id);
		}
		return $this->compconstructor($this->id, $this->year, $this->season);
	}
	
	public function get_id() {
		return $this->id;
	}
	
	public function get_department() {
		return $this->department;
	}
	
	public function get_number() {
		return $this->number;
	}
	
	public function get_name() {
		return $this->name;
	}
	
	public function get_description() {
		return $this->description;
	}
	
	public function get_year() {
		return $this->year;
	}
	
	public function get_season() {
		return $this->season;
	}
	
	public function get_currpeople($in_id, $in_year, $in_season){
                $this->currcourse($in_id, $in_year, $in_season);
                return $this->currentpeople;
        } 
        
        public function get_pastpeople(){
               	$this->pastcourse();
                return $this->pastpeople;
        }
	
	public function check_match($in_courseid, $in_year, $in_season) {
		if($in_courseid==$in_id && $in_year==$in_id && $in_season==$season) {
			return true;
		}
		return false;
	}
	
	public function get_numcurrpeople(){
                return count($this->currentpeople);
        }
        
        public function get_numpastpeople(){
                return count($this->pastpeople);
        }
	
	//this function makes a course using only a course id.
	//it returns true if it works, false if it doesn't work
	public function simpconstruct($in_id) {
		$db = new Database();
		$db->connect();
		$this->id=$in_id;
		$sql="SELECT * FROM courses WHERE id = $this->id";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		$db->close();
		if(mysql_num_rows($result)==0) {
			$error="That course does not exist.";
			return false;
		}
		
		$row=mysql_fetch_array($result);
		$this->department=$row['department'];
		$this->number=$row['number'];
		$this->name=$row['name'];
		$this->description=$row['description'];
		//$this->currentpeople = get_currpeople($in_id, $in_year, $in_season);
        //$this->pastpeople = get_pastpeople($in_id, $in_year, $in_season);
        //$this->numcurrentpeople = get_numcurrpeople();
        //$this->numpastpeople = get_pastpeople();
		
		return true;
	}
	
	//this function makes a course using a course id, and the year and season for when it was taken.  Needs a course id, and the year and season when the course was taken
	//it returns true if it works, false if it doesn't work
	public function compconstructor($in_id, $in_year, $in_season) {
		$db = new Database();
		$db->connect();
		$this->id=$in_id;
		$sql="SELECT * FROM courses WHERE id = $this->id";
		//echo $sql;
		//echo "\n";
		$result = mysql_query($sql, $db->connection()) or die(error_log(mysql_error()));
		$db->close();
		if(mysql_num_rows($result)==0) {
			$this->error="That course does not exist.";
			return false;
		}
		
		$row=mysql_fetch_array($result);

		$this->department=$row['department'];
		$this->number=$row['number'];
		$this->name=$row['name'];
		$this->description=$row['description'];
		$this->year=$in_year;
		$this->season=$in_season;
                $this->currentpeople = $this->get_currpeople($in_id, $in_year, $in_season);
                $this->pastpeople = $this->get_pastpeople();
                $this->numcurrentpeople = $this->get_numcurrpeople();
                $this->numpastpeople = $this->get_pastpeople();

		return true;
	}

	//this function finds people who are currently taking a course
	public function currcourse($in_id, $in_year, $in_season){
                $db = new Database();
		$db->connect();
		$this->id=$in_id;
		$this->year=$in_year;
		$this->season=$in_season;
		$currpeople = array();
		$sql = "SELECT people_rcsid FROM took_class WHERE course_id = '$this->id' AND year = '2011' AND season ='spring'";
		$result = mysql_query($sql, $db->connection()) or die(error_log(mysql_error()));
		$db->close();
		if(mysql_num_rows($result)==0) {
			$this->error="That course does not exist.";
			return false;
		}

		while ($row=mysql_fetch_array($result)) {
			$currpeople[] = $row['people_rcsid'];
		}
		error_log("I'm about to exit");
                $this->currentpeople = $currpeople;
                return true;
        }
 
        public function pastcourse(){

                $db = new Database();
		$db->connect();
		$pastpeople = array();
        $sql = "SELECT people_rcsid FROM took_class WHERE course_id = '$this->id' AND year <> '2011' AND season <> 'spring'";
       	$result = mysql_query($sql, $db->connection()) or die(error_log(mysql_error()));

		if(mysql_num_rows($result)==0) {
			$this->error="That course does not exist.";
			return false;
		}

		while ($row=mysql_fetch_array($result)) {
			$pastpeople[] = $row['people_rcsid'];
		}
                $this->pastpeople = $pastpeople;

                $db->close();
                return true;
        }
};



?>