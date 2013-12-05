<?php session_start(); ?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>CloudFlix</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <!-- Latest compiled and minified CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Latest compiled and minified JavaScript -->
    <script src="js/bootstrap.min.js"></script>

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
  <?php
echo exec("python s3Downloader.py ".$_SESSION['uid']);
echo exec("chmod 777 recommend_".$_SESSION['uid'].".dat");
$file = fopen("recommend_".$_SESSION['uid'].".dat", "r") or exit("Unable to open file!");
//Output a line of the file until the end is reached
$movies = array();

while(!feof($file))
  {
    $movies[]=fgets($file);
  }
fclose($file);
//echo $movies[1];
$num = sizeof($movies)<6?sizeof($movies):6;

$rand_keys = array_rand($movies, $num);
//echo $rand_keys[1];
//$rand_keys = array_rand($movies,2);

$con = mysqli_connect(localhost,root,"password",CloudFlix);

// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"select * from movies where mid in (".$movies[$rand_keys[0]].",".$movies[$rand_keys[1]].",".$movies[$rand_keys[2]].",".$movies[$rand_keys[3]].",".$movies[$rand_keys[4]].",".$movies[$rand_keys[5]].")");

$mid = array();
$mname = array();
$mlink = array();
$year = array();

while($row = mysqli_fetch_array($result))
{
  $mid[] = $row['mid'];
  $mname[] = $row['mname'];
  $mlink[] = $row['mlink'];
  $year[] = $row['year'];
}


mysqli_close($con);

?>
    <div class="container">
      <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
      <!-- Brand and toggle get grouped for better mobile display -->
      <div class="navbar-header">
        <a class="navbar-brand" href="#">CloudFlix</a>
      </div>

      <!-- Collect the nav links, forms, and other content for toggling -->
      <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
        <ul class="nav navbar-nav">
          <li><a href="#">Recent Release</a></li>
          <li><a href="#">Top Rated</a></li>
        </ul>
        <form class="navbar-form navbar-left" role="search">
          <div class="form-group">
            <input type="text" class="form-control" placeholder="Search">
          </div>
          <button type="submit" class="btn btn-default"><span class="glyphicon glyphicon-search"></span> Search</button>
        </form>
        <ul class="nav navbar-nav navbar-right">
          <li><a href="http://54.200.142.140/d3visuals/ChartBuilder.php">Movie Trend</a></li>
          <li><a href="#">Welcome <?php echo $_SESSION['uid']; ?></a></li>
          <li><a href="MyHomePage.php">Logout</a></li>
        </ul>
      </div><!-- /.navbar-collapse -->
    </nav>
    </div>
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <center><img src="img/cloudFlix_logo.png" style="height:130px; margin-top:70px" /></center>
          <hr />
          <div class="row">

            <div class="col-md-2">
            <div class="thumbnail">
              <img src="img/unavailable.png" style="height: 200px; margin-top:10px" />
              <div class="captio">
                <b><?php echo $mname[0]." (".$year[0].")";?></b>
                <p>
                  <a href="#" class="btn btn-success" role="button"><span class="glyphicon glyphicon-thumbs-up"></span></a> 
                  <a href="#" class="btn btn-danger" role="button"><span class="glyphicon glyphicon-thumbs-down"></span></a>
                </p>
              </div>
            </div>
            </div>

           <div class="col-md-2">
            <div class="thumbnail">
              <img src="img/unavailable.png" style="height: 200px; margin-top:10px" />
              <div class="caption">
		<b><?php echo $mname[1]." (".$year[1].")";?></b>
                <p>
                  <a href="#" class="btn btn-success" role="button"><span class="glyphicon glyphicon-thumbs-up"></span></a> 
                  <a href="#" class="btn btn-danger" role="button"><span class="glyphicon glyphicon-thumbs-down"></span></a>
                </p>
              </div>
            </div>
            </div>

            <div class="col-md-2">
            <div class="thumbnail">
	      <img src="img/unavailable.png" style="height: 200px; margin-top:10px" />	
              <div class="caption">
                <b><?php echo $mname[2]." (".$year[2].")";?></b>
		<p>
                  <a href="#" class="btn btn-success" role="button"><span class="glyphicon glyphicon-thumbs-up"></span></a> 
                  <a href="#" class="btn btn-danger" role="button"><span class="glyphicon glyphicon-thumbs-down"></span></a>
                </p>
              </div>
            </div>
            </div>

            <div class="col-md-2">
            <div class="thumbnail">
	      <img src="img/unavailable.png" style="height: 200px; margin-top:10px" />
              <div class="caption">
                <b><?php echo $mname[3]." (".$year[3].")";?></b>
		<p>
                  <a href="#" class="btn btn-success" role="button"><span class="glyphicon glyphicon-thumbs-up"></span></a> 
                  <a href="#" class="btn btn-danger" role="button"><span class="glyphicon glyphicon-thumbs-down"></span></a>
                </p>
              </div>
            </div>
            </div>

            <div class="col-md-2">
            <div class="thumbnail">
		<img src="img/unavailable.png" style="height: 200px; margin-top:10px" />
              <div class="caption">
		<b><?php echo $mname[4]." (".$year[4].")";?></b>
                <p>
                  <a href="#" class="btn btn-success" role="button"><span class="glyphicon glyphicon-thumbs-up"></span></a> 
                  <a href="#" class="btn btn-danger" role="button"><span class="glyphicon glyphicon-thumbs-down"></span></a>
                </p>
              </div>
            </div>
            </div>

            <div class="col-md-2">
            <div class="thumbnail">
		<img src="img/unavailable.png" style="height: 200px; margin-top:10px" />
              <div class="caption">
		<b><?php echo $mname[5]." (".$year[5].")";?></b>
                <p>
                  <a href="#" class="btn btn-success" role="button"><span class="glyphicon glyphicon-thumbs-up"></span></a> 
                  <a href="#" class="btn btn-danger" role="button"><span class="glyphicon glyphicon-thumbs-down"></span></a>
                </p>
              </div>
            </div>
            </div>

        </div>
        <hr />
<?php echo $mlink[0]; echo $mid[0]; ?>
          <center><small>Copyright &copy; CloudFlix USA 2013</small></center>
      </div>
  </body>
</html>
