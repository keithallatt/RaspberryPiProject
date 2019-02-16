<html>
<head>
	<meta charset="UTF-8">
	<title>RPP</title>
	<link type="text/css" rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css?version=5">
	<link type="text/css" rel="stylesheet" href="styles.css?version=15">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
</head>
<body>

<nav class="navbar-inverse">
<div class="container-fluid">
<div class="navbar-header">
<a class="navbar-brand" href="http://192.168.2.45/index.php">RPP</a>
</div>
<ul class="nav navbar-nav">
<li class="active"><a href="http://192.168.2.45/index.php"> Home </a></li>
<li><a href="http://192.168.2.45/rpp_hub.html">rpi0</a></li></ul>
</div>
</nav>
	
<div class="container"><h1> Raspberry Pi Project <img src="https://seeklogo.com/images/R/raspberry-pi-logo-8240ABBDFE-seeklogo.com.png" alt="RasPi Logo" width=49 height=60> </h1></div>
 
<div class="form-group container">
<form action="upload.php" method="post" enctype="multipart/form-data">
File Submissions (Python Scripts and XML Tasks): 
	<br />
	Select File to Upload: <br />
	<div align="center" >
		<input type="file" name="fileToUpload" id="fileToUpload">
	</div> <br />

	<input class="form-control" type="submit" value="Upload" name="submit" />
</form>
</div>
<div class="container"><h3>Read Me</h3></div><div class="container"><p>
<br />
This is a project designed to take control of a RPi to schedule, and complete tasks. The way this will be achieved through a scheduling task that will run every specified time interval. When this happens, the script will check for a new task to be run. If there is a new task, it will execute. When the script is executing a task, no other tasks are allowed to run. With enough RPis, using SSH, we should be able to auto distribute tasks (Explained Later)<br />
<br />
Each task will consist of some input data, either a single instance or a list, and a given script. In a bin folder (TBA), a given task will be formatted as an xml or other markup language, where parsing is easy. A field labeled &#x27;script&#x27; will contain a path to the script to be executed. Each &#x27;input&#x27; tagged field will contain a set of data that will be parsed and passed to the script, and the script, input and output will be stored in a row of output, to be checked later.<br />
<br />
For low volume tasks, such as home use, 1 to 2 tasks every hour should be enough, unless the input sizes are very large. To accomodate this, the scheduler will have to guage data input size and make appropriate choices as to how to change timing to better accomodate the number of tasks (Idle time should be minimized).<br />
<br />
If one given RPi in a pseudo-cluster is loaded with a lot of tasks, that RPi should be able to SSH into another RPi, send the file, verify it was sent correctly (ask the RPi to send the file back, if it matches, then success), and have the other RPi handle the task. This is to cut down on the backlog on any given RPi.<br />
<br />
<br />

</p></div>
<div class="container"><h3>XML Formatting</h3></div><div class="container"><p>
Task formatting is extremely important, as without proper formatting, the software cannot guess what is meant in each file. The file format is not complicated though, and merely uses a common markup language to structure. The markup language XML allows for the structure required for tasks. Each task follows this same structure.<br />
<br />
For the sake of the python script being used, any spaces will be removed automatically, but for ease of use, not using any just makes finding the task later easier.<br />
<br />
Sample.xml:<br />
-------------------<br />
<br />
&lt;?xml version=&quot;1.0&quot;?&gt;<br />
&lt;task name=&quot;SampleTaskName&quot;&gt;<br />
	&lt;script name=&quot;SampleTaskScript.py&quot; /&gt;<br />
	&lt;input_list&gt;<br />
		&lt;input type=&quot;int/float/etc&quot; value=&quot;value of input&quot; /&gt;<br />
		...<br />
	&lt;/input_list&gt;<br />
&lt;/task&gt;<br />
<br />
-------------------<br />
<br />
The parser for these xml files is procedural, meaning inputs are logged in order. This means programming the scripts to handle given inputs is facilitated slightly (i.e. there is no searching or sorting the inputs necessary).<br />
<br />
<br />

</p></div>
<div class="container"><h3>Python Formatting</h3></div><div class="container"><p>
Each python script requires some built in packages for them to work efficiently. Using a few scripts from the custom dependencies package, accepting input and basic tasks become more user friendly. <br />
<br />
Sample.py<br />
-------------------<br />
<br />
from dependencies import task_dependencies<br />
from dependencies import run_task<br />
<br />
import sys<br />
<br />
name, script, inputs = run_task.parseXML(sys.argv[1])<br />
<br />
...<br />
<br />
print(output)<br />
<br />
-------------------<br />
<br />
In each file, by importing the Run Task script, we now have access to the inputs being parsed for the given task. Importing the Task Dependencies script holds less crucial, but more useful functions, for example: the function __get_time_run__() returns the time the code was run, giving a better idea of when the task was being completed. These functions are not necessary, but more useful to give more responsive output. In future, more functions will be added to the dependencies package. For use, these are the only packages that should be imported for access to processable input.<br />
<br />

</p></div>
</body>
</html>
