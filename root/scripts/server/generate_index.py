"""
Generate the index.php file. This will contain a file upload php script
and log in box (so unauthorized use is not allowed).

@author: Keith Allatt

"""
import os
import random
import html

import urllib.request

# this is where the css sheets for all pages for this server.
# these are all inside /var/www/html or online
universal_css_sheets = [
	"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css", 
	"styles.css"
]
universal_scripts = [
	"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js",
	"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"
]

mkfile = "/var/www/html/index.php"

documentation_dir = "/var/www/html/documentation/"

host_conf = "/root/rpp.conf"

conf_contents = open(host_conf,'r').read()
d = {}
exec(conf_contents, d)
		
hosts = d["hosts"]
master = d["master"]
this_node = d["this_node"]

def gen_nav_bar():
	# this is index so, link master

	mid = '''
<nav class="navbar-inverse">
<div class="container-fluid">
<div class="navbar-header">
<a class="navbar-brand" href="http://'''+hosts[master]+'''/index.php">RPP</a>
</div>
<ul class="nav navbar-nav">
'''	
	mid += "<li class=\"active\"><a href=\"http://"+hosts[master]+"/index.php\"> Home </a></li>\n"
	
	mid += "\n".join([
		"<li><a href=\"http://"+hosts[node_name]+"/rpp_hub.html\">"+node_name+"</a></li>" 
			for node_name in hosts])

	mid +='''</ul>
</div>
</nav>
	'''
	
	return mid


def gen_head():
	global universal_css_sheets
	open_tag = "<head>\n"
	close_tag = "</head>\n"
	
	meta_tag = "\t<meta charset=\"UTF-8\">\n"
	title_tag = "\t<title>RPP</title>\n"

	css_tag = lambda sheet: "\t<link type=\"text/css\" rel=\"stylesheet\" href=\"" + sheet + "?version="+str(random.randrange(1,101))+"\">\n"

	css_tags = "".join([css_tag(s) for s in universal_css_sheets])

	script_tag = lambda sheet: "\t<script src=\""+sheet+"\"></script>\n"
	
	script_tags = "".join([script_tag(s) for s in universal_scripts])
	return  open_tag + \
			meta_tag + \
			title_tag + \
			css_tags + \
			script_tags + \
			close_tag

def gen_file_submit_form():
	# get diagnostic forms and find the right upload.php
	#upload_php_loc = None
	#min_num_tasks = None
	#for host_name in hosts:
	#	try:
	#		ip_addr = hosts[host_name]
	#		fp = urllib.request.urlopen("http://"+ip_addr+"/__diagnostic__.out")
	#		mybytes = fp.read()
	#		mystr = mybytes.decode("utf8")
	#		fp.close()
	#		num_tasks = int(mystr)
	#		
	#		if upload_php_loc is None:
	#			upload_php_loc = hosts[host_name]
	#			min_num_tasks = num_tasks
	#		elif num_tasks < min_num_tasks:
	#			upload_php_loc = hosts[host_name]
	#			min_num_tasks = num_tasks
	#	except urllib.error.URLError:
	#		print("Cannot reach host: "+host_name)	
	
	file_submit_form = '''
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
'''
	return file_submit_form

def gen_documentation():
	mid = ""
	
	doc_files = os.listdir(documentation_dir)
	doc_files.sort()	

	for f in doc_files:
		_file = documentation_dir + f
		
		if f.endswith(".txt"):
			file_name_mod = " ".join(f[:-4].split("_")[1:]).title()
		
			# special cases here 
			# Xml -> XML
			file_name_mod = file_name_mod.replace("Xml", "XML")
	
			mid += "<h3>" + file_name_mod + "</h3>"

			contents = open(_file,"r").read()
			# escape contents	
			mid += "<p>\n"+html.escape(contents).replace("\n", "<br />\n")+"\n</p>\n"
		else:
			mid += "<a href=\"documentation/"+f+"\"><p>"+f+"</p></a><br />\n"
    
	return mid

def gen_body():
	time_formatting = "%d %b %Y %H:%M:%S"

	open_tag = "<body>\n"
	close_tag = "</body>\n"
	
	mid = ""

	mid += gen_nav_bar()

	# png is 245 by 300 originally, going with 49 by 60
	mid += """
<h1> Raspberry Pi Project <img src="https://seeklogo.com/images/R/raspberry-pi-logo-8240ABBDFE-seeklogo.com.png" alt="RasPi Logo" width=49 height=60> </h1>
 """
	
	mid += gen_file_submit_form()
	
	mid += gen_documentation()
	
	return open_tag + mid + close_tag

def gen_html():
	open_tag = "<html>\n"
	close_tag = "</html>\n"

	html_ = open_tag + gen_head() + gen_body() + close_tag

	html_ = html_.replace("<p>",  "<div class=\"container\"><p>")
	html_ = html_.replace("</p>", "</p></div>")

	html_ = html_.replace("<h1>",  "<div class=\"container\"><h1>")
	html_ = html_.replace("</h1>", "</h1></div>")

	html_ = html_.replace("<h3>",  "<div class=\"container\"><h3>")
	html_ = html_.replace("</h3>", "</h3></div>")

	return html_


f = open(mkfile, "w")
f.write(gen_html())
f.close()
