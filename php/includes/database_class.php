<?php

class Database {
	// Property Declarations
	private $db_name;
	private $host;
	private $user;
	private $pass;	
	
	private $connection;
	
	function __construct() {
		$this->db_name = "camarr_StudentCity";
		$this->host = "localhost";
		$this->user = "camarr_sc";
		$this->pass = "ArS5L}$,{xt_";
	}
	
	public function connect() {
		$connection = mysql_connect($this->host, $this->user, $this->pass) or die(mysql_error());
		if ( !mysql_select_db($this->db_name, $connection) ) {
			echo "Could not connect to database | " . mysql_error();
		}
		
		$this->connection = $connection;
	}
	
	public function close() { mysql_close( $this->connection ); }
	
	public function connection() { return $this->connection; }
}

?>