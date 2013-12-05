<?php

$con = mysqli_connect(localhost,root,"password",CloudFlix);



// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"SELECT * FROM login where username = '".$_POST["uname"]."'");

if($row = mysqli_fetch_array($result))
{

  if($row['password'] == $_POST["pwd"]){
    session_start();
    $_SESSION['uid']=$row['userid'];
    echo "Redirecting...";
  }
  else
    echo "Please enter correct username or password. Redirecting in 3 seconds.";
                        ?><meta http-equiv="refresh" content="3; url=UserPage.php"><?php
}
mysqli_close($con);
/*$connection = oci_connect($username = 'ugoel',
                          $password = 'MICROSOFT123!',
                          $connection_string = '//oracle.cise.ufl.edu/orcl');
$statement = oci_parse($connection, 'SELECT * FROM UGOEL.ACCOUNTS where ACCOUNT_ID = \''.$_POST["username"].'\'');
oci_execute($statement);

if($row = oci_fetch_object($statement))
{
		if($row->ACCOUNT_PASSWORD==$_POST["password"])
		{
			echo "Redirecting";

			session_start();
			$_SESSION['account_record']=$row;

			if($row->ACCOUNT_TYPE == 'residents') {
			$statement1 = oci_parse($connection, 'SELECT * FROM UGOEL.residents where ACCOUNT_ID = \''.$_POST["username"].'\'');
			oci_execute($statement1);
			$row1 = oci_fetch_object($statement1);
			$_SESSION['resident_record']=$row1;
			echo "<meta http-equiv=\"refresh\" content=\"0; url=resident.php\">";
			}
			else if($row->ACCOUNT_TYPE == 'FIN'){
			echo "<meta http-equiv=\"refresh\" content=\"0; url=financial_assistant.php\">";
			}
			else if($row->ACCOUNT_TYPE == 'ASSTM'){
			echo "<meta http-equiv=\"refresh\" content=\"0; url=assistant_manager.php\">";
			}
		}
		else
		{ 
			echo "Please enter correct username or password. Redirecting in 3 seconds.";
			?><meta http-equiv="refresh" content="3; url=index.php"><?php
		}
}
else
{
	echo "Please enter correct username or password. Redirecting in 3 seconds.";
	?><meta http-equiv="refresh" content="3; url=index.php"><?php
	
}



while (($row = oci_fetch_object($statement))) {
	var_dump($row);
	if($row->USERNAME==$_POST["username"] && $row->PASS==$_POST["password"])	{

		echo $row->USERNAME;
		echo $row->PASS;
	echo "Welcome";
	
	}



oci_free_statement($statement);
oci_close($connection);
*/
?>
