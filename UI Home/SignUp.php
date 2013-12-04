<!DOCTYPE html>
 
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta content="width=device-width, initial-scale=1.0" name="viewport">
	<meta content="" name="description">
	<meta content="" name="author">
	<link href="" rel="shortcut icon">
 
	<title>Sign Up page</title><!-- Bootstrap core CSS -->
	<link href="css/bootstrap.css" rel="stylesheet">
	<link href="css/bootstrap-responsive.css" rel="stylesheet">
</head>
 
<body>
    
	<div class="container">
	    <div class ="title" style ="height : 180px;">
		<img src="images/143.png" style ="width : 100%; height : 100%;" alt="Demo2 second" title="Demo2 second" usemap="#img1map1"/>
		</div>
		<div class="well" >
			<form action="register.php" class="form-horizontal well" method="post">
				<fieldset>
					<legend>Sign Up</legend>
 
					<h4>It’s free and always will be.</h4>
 
					<div class="row">
						<div class="col-xs-8">
							<div class="form-group">
								<div class="rows">
									<div class="col-md-8">
										<div class="col-lg-6">
											<input class="form-control input-lg" id="fName" name=
											"fName" placeholder="First Name" type="text">
										</div>
 
										<div class="col-lg-6">
											<input class="form-control input-lg" id="lName" name=
											"lName" placeholder="Last Name" type="text">
										</div>
									</div>
								</div>
							</div>
 
							<div class="form-group">
								<div class="rows">
									<div class="col-md-8">
										<div class="col-lg-12">
											<input class="form-control input-lg" id="email" name=
											"email" placeholder="Your Email" type="text">
										</div>
									</div>
								</div>
							</div>
 
							<div class="form-group">
								<div class="rows">
									<div class="col-md-8">
										<div class="col-lg-12">
											<input class="form-control input-lg" id="reemail" name=
											"reemail" placeholder="Re-enter Email" type="text">
										</div>
									</div>
								</div>
							</div>
 
							<div class="form-group">
								<div class="rows">
									<div class="col-md-8">
										<div class="col-lg-12">
											<input class="form-control input-lg" id="password"
											name="password" placeholder="New Password" type=
											"password">
										</div>
									</div>
								</div>
							</div>
 
							<div class="form-group">
								<div class="rows">
									<div class="col-md-8">
										<h4></h4>
 
										<div class="col-md-3">
									
											<!--<h4><label class=
											"col-lg-4 control-label">Birthday</label> </h4>
 
											<div class="col-lg-3">
												<h4><select class="form-control input-sm" name=
												"month">
													<option>
														Month
													</option>
													<!--php code for populating the selectbox for Month -->
							<!--					</select> </h4>
 
												<div class="col-lg-3">
													<h4><select class="form-control input-sm" name=
													"day">
														<option>
															Day
														</option>
														<!--php code for populating the selectbox for Day -->
								<!--					</select> </h4>
 
													<div class="col-lg-3">
														<h4><select class="form-control input-sm"
														name="year">
															<option>
																Year
															</option>
															<!--php code for populating the selectbox for Year -->
									<!--					</select> </h4>
													</div>
												</div>
											</div> -->
										</div>
									</div>
								</div>
							</div>
 
							<div class="form-group">
								<div class="rows">
									<div class="col-md-4">
										<div class="col-lg-6">
											<div class="radio">
												<label><input checked id="optionsRadios1" name=
												"optionsRadios" type="radio" value=
												"Female">Female</label>
											</div>
										</div>
 
										<div class="col-lg-6">
											<div class="radio">
												<label><input id="optionsRadios2" name=
												"optionsRadios" type="radio" value="Male">
												Male</label>
											</div>
										</div>
									</div>
								</div>
							</div>
 
							<div class="form-group">
								<div class="rows">
									<div class="col-md-8">
										<div class="col-lg-12">
											<button class="btn btn-success btn-lg" type=
											"submit">Sign Up</button>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</fieldset>
			</form>
		</div>
	</div><!-- /container -->
</body>
</html>