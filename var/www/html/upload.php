<html>
<head>
	<meta charset="UTF-16">
	<title>Upload</title>
	<link type="text/css" rel="stylesheet" href="styles.css?version=70">
</head>
<body>
<p>
<?php

$target_dir = "/var/www/html/uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);

$upload_type = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));


$upload_ok = 1;

// check if file exists
if (file_exists($target_file)) {
	echo "Sorry, file already exists.\n";
	$upload_ok = 0;
}


// allow only xml and py, for now
if ($upload_type != "py" && $upload_type != "xml") {
	if ($upload_type != "pdf" && $upload_type != "txt") {
		echo "Sorry, only Python scripts and XML files allowed.\n";
		$upload_ok = 0;
	} else {
		echo "Adding to documentation.\n";
		$target_dir = "/var/www/html/documentation/";		
	}
}

// create target file from target dir.
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);

// check if upload ok
if ($upload_ok == 0) {
	echo "Sorry, your file was not uploaded.\n";
} else {
	if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
		echo "The file ". basename($_FILES["fileToUpload"]["name"]). " has been uploaded.\n";
 	} else {
		echo "Sorry, there was an error uploading your file.\n";
	}
}

?>
</p>
<a href="index.php"> <p> Back to Home </p> </a>
<a href="rpp_hub.html"> <p> To RPP Page </p> </a>
</body>
</html>
