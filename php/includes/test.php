
<?php

require_once("person.php");

$person = new Person();
echo $person->login("helleb2", "donuts");
//echo $person->login("helleb2", "donut");
//echo $person->profile_update("Testy", "Testerson", 2012, "Web Science", "IT", 0, 1, 0);
//echo $person->get_emailst();
echo $person->get_friends();
echo $person->add_friend("test");
echo $person->get_friends();
echo $person->remove_friend("test");
echo $person->get_friends();

//passwords: helleb2:donuts		labuza:unicorn		test:testtest
?>