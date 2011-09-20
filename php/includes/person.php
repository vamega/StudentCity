<?php

require_once("database_class.php");
require_once("course.php");
class Person
{
	private $fname;
	private $lname;
	private $year;
	private $sex;
	private $major;
	private $major2;
	private $currentclassst;  //boolean value of whether the user wants their current classes to be publically available
	private $emailst;	//boolean value of whether the user wants their email address to be publically available
	private $picst;		//boolean value of whether the user wants their profile picture to be publically available
	private $allcourses;		//array of courses: all the courses the student has ever taken, past + present
	private $currentcourses;	//array of courses: the courses the student is currently taking, in the present
	public $error;
	
	private $rcsid;

	function __construct ( $rcs ) {
		$this->rcsid = $rcs;
		$this->update_class();
	}
	
	public function full_update_person() {
		return login($this->rcsid);
	}

	
	//give it a name of any sort, either a first name, a last name, or both with a space in between
	//returns an array of results
	public function search($in_name) {
		$db = new Database();
		$db->connect();
		$pos = strpos($in_name, " ");
		if($pos == false) {
			$sql = "SELECT * FROM people WHERE lower(fname) LIKE '%".strtolower($in_name)."%' OR lower(lname) LIKE '%".strtolower($in_name)."%'";
		}
		
		else {
			$temparray = explode(" ", $in_name);
			$sql = "SELECT * FROM people WHERE lower(fname) LIKE '%".strtolower($temparray[0])."%' OR lower(lname) LIKE '%".strtolower($temparray[1])."%'";
		}
		
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		if(mysql_num_rows($result) == 0) {
			$this->error = "No people results were found for that search term";
			return false;
		}
		
		while ($row = mysql_fetch_array($result)) {
			$temp = new Person( $row['RCSid'] );
			$tcurrentcourses[] = $temp;
		}
		
		return $tcurrentcourses;
	}
	
	public function update_class() {
		$db = new Database();
		$db->connect();
		$sql = "SELECT * FROM people WHERE RCSid = '".$this->rcsid."'";
		$result = mysql_query($sql, $db->connection())  or die(mysql_error());
		//$db->close();
		if(mysql_num_rows($result) == 0) {
			$this->error="That RCSid or the password is incorrect.";
			//echo "That RCSid or the password is incorrect.";
			return false;
		}
		
		$row = mysql_fetch_array($result);
		
		$this->fname = $row["fname"];
		$this->lname = $row["lname"];
		$this->year =  $row["class_year"];
		$this->major = $row["major"];
		$this->major2 = $row["major2"];
		$this->picst = $row["profile_pic"];
		$this->currentclassst = $row["current_classes"];
		$this->emailst = $row["email_messages"];
		$this->rcsid = $row["RCSid"];
	}
			
			
			
//this function unsigns a person up for a class.  It needs the course id, as well as the year and season the person took the class in.
//this function returns a true if it works, and a false if it doesn't.	
	public function delete_course($in_courseid, $in_year, $in_season) {
		$db = new Database();
		$db->connect();
		$sql="SELECT * FROM took_class WHERE course_id=$in_courseid AND people_rcsid='".$this->rcsid."' AND year=$in_year AND season='".$in_season."'";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		if(mysql_num_rows($result) == 0) {
			$this->error="That person has not taken that course in that semester.";
			//echo "That person has not taken that course in that semester.";
			return false;
		}
		
		$sql="DELETE FROM took_class WHERE course_id=$in_courseid AND people_rcsid='".$this->rcsid."' AND year=$in_year AND season='".$in_season."'";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		if ( !$result ) {
			$this->error = "Something went wrong while deleting from the database.";
			//echo "Something went wrong while deleting from the database.";
			return false;
		}
		
				if(sizeof($this->allcourses) > 0) {
			foreach ($this->allcourses as $thing) {
				unset($thing);
			}
		}
		
		if (sizeof($this->currentcourses) > 0) {
			foreach ($this->currentcourses as $thing) {
				unset($thing);
			}
		}
		$tallcourses=array();
		$tcurrentcourses=array();
		$sql="SELECT * FROM took_class WHERE people_rcsid='".$this->rcsid."'";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		$db->close();
		while ($row=mysql_fetch_array($result)) {
			$temp = new Course();
			//echo "all!\n".$temp->get_id()."\n";
			$temp->compconstructor($row['course_id'], $row['year'], $row['season']);
			$tallcourses[] = $temp;
		}
		
		$sql="SELECT * FROM took_class WHERE year=2011 AND season='spring' AND people_rcsid='".$this->rcsid."'";
		//echo $sql;
		//echo "\n";	
		//echo $db->connection();
		$db2 = new Database();
		$db2->connect();
		$result = mysql_query($sql, $db2->connection()) or die(mysql_error());

		$db2->close();		
		while ($row=mysql_fetch_array($result)) {
			$temp = new Course();
			//echo "current!\n".$temp->get_id()."\n";
			$temp->compconstructor($row['course_id'], $row['year'], $row['season']);
			$tcurrentcourses[] = $temp;

		
		}
		$this->allcourses = $tallcourses;

		$this->currentcourses = $tcurrentcourses;
		//echo "\n";
		//foreach ($this->allcourses as $thing) {
			//echo $thing->get_id();
			//echo "\n";
		//}
		
		//foreach ($this->currentcourses as $thing) {
			//echo $thing->get_id();
			//echo "\n";
		//}
		//print_r($this->allcourses);
		//print_r($this->currentcourses);
		return true;
	}
		
		
	//this function signs a person up for a course.  it needs the course id, as well as the year and season that the user is taking the course.
	//this function returns true if it works, and false if it doesn't
	public function add_course($in_courseid, $in_year, $in_season) {	//Jeff: what about adding classes that the user has taken in the past?
		$db = new Database();
		$db->connect();
		//echo $db->connection();
		$db3 = new Database();
		$db3->connect();
		//echo "The other one".$db3->connection();
		$this->error="";
		
		$sql="SELECT * FROM took_class WHERE people_rcsid='".$this->rcsid."' AND course_id='".$in_courseid."' AND year=$in_year AND season='".$in_season."'";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		if(mysql_num_rows($result)==1) {
			$this->error="That user is already entered in that class in that time period.";
			//echo "That user is already entered in that class in that time period.";
			return false;
		}
		
		$sql="INSERT INTO took_class (course_id, people_rcsid, year, season) VALUES ($in_courseid, '".$this->rcsid."', $in_year, '".$in_season."')";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		if ( !$result ) {
			$this->error = "Something went wrong while inputting into the database.";
			return false;
		}
		if(sizeof($this->allcourses) > 0) {
			foreach ($this->allcourses as $thing) {
				unset($thing);
			}
		}
		
		if (sizeof($this->currentcourses) > 0) {
			foreach ($this->currentcourses as $thing) {
				unset($thing);
			}
		}
		$tallcourses=array();
		$tcurrentcourses=array();
		$sql="SELECT * FROM took_class WHERE people_rcsid='".$this->rcsid."'";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		$db->close();
		while ($row=mysql_fetch_array($result)) {
			$temp = new Course();
			//echo "all!\n".$temp->get_id()."\n";
			$temp->compconstructor($row['course_id'], $row['year'], $row['season']);
			$tallcourses[] = $temp;
		}
		
		$sql="SELECT * FROM took_class WHERE year=2011 AND season='spring' AND people_rcsid='".$this->rcsid."'";
		//echo $sql;
		//echo "\n";	
		//echo $db->connection();
		$db2 = new Database();
		$db2->connect();
		$result = mysql_query($sql, $db2->connection()) or die(mysql_error());

		$db2->close();		
		while ($row=mysql_fetch_array($result)) {
			$temp = new Course();
			//echo "current!\n".$temp->get_id()."\n";
			$temp->compconstructor($row['course_id'], $row['year'], $row['season']);
			$tcurrentcourses[] = $temp;

		
		}
		$this->allcourses = $tallcourses;

		$this->currentcourses = $tcurrentcourses;
		//echo "\n";
		//foreach ($this->allcourses as $thing) {
			//echo $thing->get_id();
			//echo "\n";
		//}
		
		//foreach ($this->currentcourses as $thing) {
			//echo $thing->get_id();
			//echo "\n";
		//}
		//print_r($this->allcourses);
		//print_r($this->currentcourses);
		return true;
	}
	

	//this function creates a person/passsword combo in the database.  It needs an rcsid and a password.
	//this function returns true if it worked, and false if it did not work.
	public function register($in_rcsid, $in_password) { 
		
		$this->error="";
		$this->fname="";
		$this->lname="";
		$this->year="";
		$this->major="";
		$this->major2="";
		$this->pic="";
		
		$db = new Database();
		$db->connect();
		
		$sql = "SELECT * FROM people WHERE RCSid = '".$in_rcsid."'";

		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		if(mysql_num_rows($result)==1) {
			$this->error="That RCSID $in_rcsid already has an account.";
			return false;
		}

		$confirm_code = $this->confirm_email($in_rcsid);
		
		if( $confirm_code ){
			$this->rcsid=$in_rcsid;
			$sqlinsert = "INSERT INTO people (RCSid, password, confirm_code) VALUES ('$this->rcsid','".md5($in_password)."', '$confirm_code')";
			$result = mysql_query($sqlinsert, $db->connection()) or die(error_log(mysql_error()));
			$db->close();

			if ( !$result ) {
				$this->error = "Something went wrong while inputting into the database.";
				return false;
			}
		}
		
		else {
			$this->error = "Oops. There was a problem sending your confirmation.";
			return false;
		}
			
		
		$allcourses = array();
		$currentcourses = array();
		
		return true;
	}

	//this function retrieves all information relevant to the person.  It needs an rcsid and a password.
	//this function returns true if it worked, and false if it did not.
	public function login($in_rcsid, $in_password) { 
		$db = new Database();
		$db->connect();
		$this->error="";

		$sql = "SELECT * FROM people WHERE RCSid = '".$in_rcsid."' AND password= '".md5($in_password)."'";
		$result = mysql_query($sql, $db->connection())  or die(mysql_error());
		//$db->close();
		if(mysql_num_rows($result) == 0) {
			$this->error="That RCSid or the password is incorrect.";
			//echo "That RCSid or the password is incorrect.";
			return false;
		}
		
		$row = mysql_fetch_array($result);

		if($row["confirm"] == 0) {
			$this->error = "You must confirm your registration. You should have an email with a link that will allow you to proceed. Click <a href=\"includes/resend_email.php?id=$in_rcsid\">here</a> to resend the confirmation email";
			return false;
		}
				
		$this->fname = $row["fname"];
		$this->lname = $row["lname"];
		$this->year =  $row["class_year"];
		$this->major = $row["major"];
		$this->major2 = $row["major2"];
		$this->picst = $row["profile_pic"];
		$this->currentclassst = $row["current_classes"];
		$this->emailst = $row["email_messages"];
		$this->rcsid = $row["RCSid"];
		
		//echo "Hi there!";
		//RCSid and password are a match, user can log in.
		$tallcourses=array();
		$tcurrentcourses=array();
		$sql="SELECT * FROM took_class WHERE people_rcsid='".$this->rcsid."'";
		$result = mysql_query($sql, $db->connection()) or die(error_log(mysql_error()));
		$db->close();
		while ($row=mysql_fetch_array($result)) {
			$temp = new Course();
			//echo "all!\n".$temp->get_id()."\n";
			$temp->compconstructor($row['course_id'], $row['year'], $row['season']);

			$tallcourses[] = $temp;
		}

		$sql="SELECT * FROM took_class WHERE year=2011 AND season='Spring' AND people_rcsid='".$this->rcsid."'";
		//echo $sql;
		//echo "\n";	
		//echo $db->connection();
		$db2 = new Database();
		$db2->connect();
		$result = mysql_query($sql, $db2->connection()) or die(mysql_error());

		$db2->close();		
		while ($row=mysql_fetch_array($result)) {
			$temp = new Course();
			//echo "current!\n".$temp->get_id()."\n";
			$temp->compconstructor($row['course_id'], $row['year'], $row['season']);
			$tcurrentcourses[] = $temp;

		}
		$this->allcourses = $tallcourses;

		$this->currentcourses = $tcurrentcourses;

		//echo "\n";
		//foreach ($this->allcourses as $thing) {
			//echo $thing->get_id();
			//echo "\n";
		//}
		
		//foreach ($this->currentcourses as $thing) {
			//echo $thing->get_id();
			//echo "\n";
		//}
		//print_r($this->allcourses);
		//print_r($this->currentcourses);
		
		return true;
		
	}
	
	public function update_current_courses () {
		$tcurrentcourses=array();

		$sql="SELECT * FROM took_class WHERE year=2011 AND season='Spring' AND people_rcsid='".$this->rcsid."'";
		//echo $sql;
		//echo "\n";	
		//echo $db->connection();
		$db2 = new Database();
		$db2->connect();
		$result = mysql_query($sql, $db2->connection()) or die(mysql_error());

		$db2->close();		
		while ($row=mysql_fetch_array($result)) {
			$temp = new Course();
			//echo "current!\n".$temp->get_id()."\n";
			$temp->compconstructor($row['course_id'], $row['year'], $row['season']);
			$tcurrentcourses[] = $temp;
		}

		$this->currentcourses = $tcurrentcourses;
	}
	
	//this function updates changeable data, other than rcsid and password, about a person
	//it needs, in this order, a first name, last name, graduation year, major, secondary major, does the user their profile picture to be viewed publically? (0 or 1), does the user allow their current classes to be viewed publically? (0 or 1), does the user allow their email to be viewed publically (0 or 1)
	//it returns true if it worked, false if it did not
	public function profile_update($in_fname, $in_lname, $in_year, $in_major, $in_major2, $in_pic, $in_currclass, $in_email) {
		$db = new Database();
		$db->connect();
		$this->error="";
		$this->fname=$in_fname;
		$this->lname=$in_lname;
		$this->year=$in_year;
		$this->major=$in_major;
		$this->major2=$in_major2;
		$this->picst=$in_pic;
		$this->currentclassst = $in_currclass;
		$this->emailst = $in_email;
		$sql = "UPDATE people SET fname='".$this->fname."', lname='".$this->lname."', class_year='".$this->year."', major='".$this->major."', major2='".$this->major2."', profile_pic='".$this->picst."', current_classes='".$this->currentclassst."', email_messages='".$this->emailst."' WHERE RCSid='".$this->rcsid."'";
		
		$result=mysql_query($sql, $db->connection())  or die(mysql_error());
		$db->close();
		if ( !$result ) {
			$this->error = "Something went wrong while inputting into the database.";
			return false;
		}
		return true;
}


	//this function adds a person as the user's friend, but not vice versa (can be changed, let me know).  Needs the rcsid of the new friend.
	//this function returns true if it worked, false if it did not
	public function add_friend($in_rcsid) {
		$db = new Database();
		$db->connect();
		$sql="SELECT * FROM people WHERE rcsid='".$in_rcsid."'";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		if(mysql_num_rows($result)==0) {
			$this->error="$in_rcsid is not a registered person.";
			//echo "$in_rcsid is not a registered person.";
			return false;
		}
		
		$sql="SELECT * FROM friend WHERE rcsid1='".$this->rcsid."' AND rcsid2='".$in_rcsid."'";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		if(mysql_num_rows($result)==1) {
			$this->error="$this->rcsid already lists $in_rcsid among their friends.";
			//echo "$this->rcsid already lists $in_rcsid among their friends.";
			return false;
		}
		
		$sql="INSERT INTO friend (RCSid1, RCSid2) VALUES ('".$this->rcsid."', '".$in_rcsid."')";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		$db->close();
		if(!$result) {
			$this->error="That friend insertion did not enter into the database correctly.";
			//echo "That friend insertion did not enter into the database correctly.";
			return false;
		}
		return true;
	}
	
	
	//this function removes a person as the user's friend, but not vice versa (can be changed, let me know).  Needs the rcsid of the old friend.
	//this function returns true if it worked, false if it did not
	public function remove_friend($in_rcsid) {
		$db = new Database();
		$db->connect();
		$sql="SELECT * FROM people WHERE rcsid='".$in_rcsid."'";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		if(mysql_num_rows($result)==0) {
			$this->error="$in_rcsid is not a registered person.";
			//echo "$in_rcsid is not a registered person.";
			return false;
		}
		
		$sql="SELECT * FROM friend WHERE rcsid1='".$this->rcsid."' AND rcsid2='".$in_rcsid."'";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		if(mysql_num_rows($result)==0) {
			$this->error="$this->rcsid does not currently list $in_rcsid among their friends.";
			//echo "$this->rcsid does not currently list $in_rcsid among their friends.";
			return false;
		}
		
		$sql="DELETE FROM friend WHERE RCSid1='".$this->rcsid."' AND rcsid2='".$in_rcsid."'";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		$db->close();
		if(!$result) {
			$this->error="That friend insertion did not enter into the database correctly.";
			//echo "That friend insertion did not enter into the database correctly.";
			return false;
		}
		return true;
	}
	
	
	//returns an array of all the user's friends (not people who have user listed as a friend also, can be changed)
	public function get_friends() {
		$db = new Database();
		$db->connect();
		
		$sql="SELECT * FROM friend WHERE rcsid1='".$this->rcsid."'";
		$result = mysql_query($sql, $db->connection()) or die(mysql_error());
		$db->close();
		
		$allfriends = array();
		while ($row=mysql_fetch_array($result)) {
			$allfriends[] = $row['RCSid2'];
		}
		
		//print_r($allfriends);
		return $allfriends;
	}
	
	
//returns a string of the user's full name, first and last
	public function get_full_name() {
		$space=" ";
		$go = $this->fname.$space.$this->lname;
		return $go;
	}
	
	//returns an array of classes that are all the classes that the user is currently taking.
	public function get_current_courses() {
		return $this->currentcourses;
	}
	
	//returns an array of the classes that is every class the user has taken/is taking
	public function get_all_courses() {
		return $this->allcourses;
	}
	
	public function get_first_name() {
		return $this->fname;
	}
	
	public function get_last_name() {
		return $this->lname;
	}
	
	public function get_year() {
		return $this->year;
	}
	
	public function get_major() {
		return $this->major;
	}
	
	public function get_major2() {
		return $this->major2;
	}
	
	public function get_picst() {
		return $this->picst;
	}
	
	public function get_currentclassst() {
		return $this->currentclassst;
	}
	
	public function get_emailst() {
		return $this->emailst;
	}
	
	public function get_id() {
		return $this->rcsid;
	}	
	
	public function check_confirm($in_id, $in_confirm) {
		$db = new Database();
		$db->connect();
		$id=$_GET['id'];
		$confirm = $_GET['confirm'];
		if($confirm!=md5($id.$id))
		{
			$this->error="That's not the correct confirmation code";
			return false;
		}
		$sql="UPDATE people SET confirm=1 WHERE RCSid='".$this->rcsid."'"; 
		$result = mysql_query($sql, $db->connection()) or die(error_log(mysql_error()));
		$db->close();
		if ( !$result ) {
			$this->error = "Something went wrong while updating the database.";
			return false;
		}
		
		return true;
	}
	
	public function confirm_email($id) {
		$confirm_code = md5($id.$id);
		$email = $id."@rpi.edu";
		$subject = "StudentCity Confirmation";
		
		$link = "<a href=\"http://studentcity.myrpi.org/index.php?id=$id&confirm=$confirm_code\">studentcity.myrpi.org/index.php?id=$id&confirm=$confirm_code</a>";
		$message = "<h3>Welcome to StudentCity<h3><p>This was sent to you in order to verify your email address as $email. If you did not register for StudentCity, then please disregard this message. If you would like to continue with your registration with StudentCity, please click on the following link (or copy and paste it into your browser).</p><p>$link</p><p>If you are having problems with this confirmation link, please send a message to greenj12@rpi.edu expressing your concerns.</p>";
		
		$headers = "From: StudentCity Admin <greenj12@rpi.edu>\r\nContent-Type: text/html;";
		
		if(mail($email, $subject, $message, $headers)) return $confirm_code;
		else return false;
	}
};

?>