"""
Generate HTML (specifically an html file in /var/www/...)
so that the webserver reflects changes to the tasks at hand
and how they've been dealt with. Should have a list of tasks
to be done, a list of scripts, and a list of completed tasks.

@author: Keith Allatt

"""
import pathlib
import time
import math
import os
import uuid
import random
import socket

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


mkfile = "/var/www/html/rpp_hub.html"
diagfile = "/var/www/html/__diagnostic__.out"

# don't end in /
scripts_folder = "/root/scripts"
task_bin_folder = "/root/task_bin"
output_folder = "/var/www/html/output"


host_conf = "/root/rpp.conf"

def gen_nav_bar():
	conf_contents = open(host_conf,'r').read()
	d = {}
	exec(conf_contents, d)
		
	hosts = d["hosts"]
	master = d["master"]
	this_name = d["this_node"]	

	# this is rpp so, link master
	mid = '''
<nav class="navbar-inverse">
<div class="container-fluid">
<div class="navbar-header">
<a class="navbar-brand" href="http://'''+hosts[master]+'''/index.php">RPP</a>
</div>
<ul class="nav navbar-nav">
'''	
	mid += "<li><a href=\"http://"+hosts[master]+"/index.php\"> Home </a></li>\n"
	
	mid += "\n".join([
		"<li"+(" class=\"active\"" if this_name==node_name else "")+"><a href=\"http://"+hosts[node_name]+"/rpp_hub.html\">"+node_name+"</a></li>" 
			for node_name in hosts])

	mid +='''</ul>
</div>
</nav>
	'''
	
	return mid

def list_to_table_row(ls, heading=False):
	tag = "th" if heading else "td"
	return "\t<tr>\n" + "\n\t\t".join([ "<"+tag+">"+i+"</"+tag+">" for i in ls])  + "\t\n</tr>"

def gen_head():
	global universal_css_sheets
	open_tag = "<head>\n"
	close_tag = "</head>\n"
	
	meta_tag = "\t<meta charset=\"UTF-16\">\n"
	title_tag = "\t<title>RPP-HUB</title>\n"

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
		
def gen_body():
	time_formatting = "%d %b %Y %H:%M:%S"

	open_tag = "<body>\n"
	close_tag = "</body>\n"
	mid = ""
	
	mid += gen_nav_bar()

	#########################################
	# first scripts:
	mid += "\t<h1> Scripts </h1>\n"
	mid += "\t<table class=\"container\">\n"
	scripts_dir = pathlib.Path(scripts_folder)	
	mid += list_to_table_row(["Script Name", "Script Size", "Time Created"], True)		
	for fl in scripts_dir.glob("*.py"):
		name = str(fl).split("/")[-1]
		info = fl.stat()
		time_formatted = time.strftime(
				time_formatting, 
				time.localtime(info.st_mtime)
				)
		size = info.st_size
	
			
		unit = math.floor(math.log(size, 1024))
		unit = min(unit, 4)
		
		size /= 1024**unit		
		size = int(size)

		unit = ["B", "KB", "MB", "GB", "TB"][unit]
		
		size = str(size) + unit		

		mid += list_to_table_row([name, size, time_formatted])		

	mid += "\n\t</table>\n"
	########################################



	#########################################
	# second tasks in bin:
	mid += "\t<h1> Tasks in Bin </h1>\n"
	mid += "\t<table class=\"container\">\n"
	scripts_dir = pathlib.Path(task_bin_folder)	
	mid += list_to_table_row(["Task Name", "Task File Size", "Time Created"], True)		
	num_tasks = 0
	for fl in scripts_dir.glob("*.xml"):
		num_tasks += 1
		name = str(fl).split("/")[-1]
		info = fl.stat()
		time_formatted = time.strftime(
				time_formatting, 
				time.localtime(info.st_mtime)
				)
		size = info.st_size
		
		unit = math.floor(math.log(size, 1024))
		unit = min(unit, 4)
		
		size /= 1024**unit		
		size = int(size)

		unit = ["B", "KB", "MB", "GB", "TB"][unit]
		
		size = str(size) + unit		

		mid += list_to_table_row([name, size, time_formatted])		
	## write diagnostic file
	num_tasks = str(num_tasks)
	diagnostic_file = open(diagfile,'w')
	diagnostic_file.write(num_tasks)
	diagnostic_file.close()	

	mid += "\n\t</table>\n"
	########################################



	#########################################
	# lastly outputs:
	mid += "\t<h1> Outputs </h1>\n"
	mid += "\t<table class=\"container\">\n"
	scripts_dir = pathlib.Path(output_folder)	
	mid += list_to_table_row(["Task Name", "Output File Size", "Time Created", "Link"], True)		
	
	
	for fl in os.listdir(output_folder):
		output_file = None
		task_file = None
		
		inner_folder = output_folder+"/"+fl
		
		for inner_file in os.listdir(inner_folder):
			if inner_file[-3:] == "xml":
				task_file = inner_file
			elif inner_file[-3:] == "out":
				output_file = inner_file
		

		name = output_file[:-4]

		info = os.stat(inner_folder +"/"+output_file)

		time_formatted = time.strftime(
				time_formatting, 
				time.localtime(info.st_mtime)
				)
		size = info.st_size
		
		
		try:
			unit = math.floor(math.log(size, 1024))
			unit = min(unit, 4)
		except ValueError:
			unit = 0
			
		size /= 1024**unit		
		size = int(size)

		unit = ["B", "KB", "MB", "GB", "TB"][unit]
		
		size = str(size) + unit		

		file_name_on_server = inner_folder[6:]+"/"+name+".out"
		link_to_out = "<a href=\""+file_name_on_server+"\">Raw Output</a>"

		mid += list_to_table_row([name, size, time_formatted, link_to_out])		

	mid += "\n\t</table>\n"
	########################################

	return open_tag + mid  + close_tag

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


index_file = open(mkfile, "w")
index_file.write(gen_html())
index_file.close()

