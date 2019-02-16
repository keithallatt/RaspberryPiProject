"""
Represents the scheduler.

Will run every 10 minutes


@author: Keith Allatt
"""
import time
import os

import sys
sys.path.insert(0, "/root/scripts/dependencies")

import run_task

# for unique mapping to output space
import uuid


flag_filename = "/root/flags/taskRunning"
flag_maintenance = "/root/flags/maintenance"

create_flag = "touch "+flag_filename
remove_flag = "rm "   +flag_filename


time_format = "%a, %d %b %Y, %Z, %H:%M:%S"
time_format_condensed = "%d-%m-%Y,%Z,%H:%M:%S"

time_formatted = str(time.strftime(time_format))

time_formatted_condensed = str(time.strftime(time_format_condensed))


def hasTaskRunning():
	global flag_filename
	return os.path.isfile(flag_filename)


def isUnderMaintenance():
	global flag_maintenance
	
	if "--force" in sys.argv[1:]:
		return False

	return os.path.isfile(flag_maintenance)


if hasTaskRunning():
	print("Task Running : "+time_formatted_condensed)
	exit(1)
elif isUnderMaintenance():
	print("Is Under Maintenance : "+time_formatted_condensed)
	exit(2)

task_bin = os.listdir("/root/task_bin")

if len(task_bin) == 0:
	print("Task Bin is Empty. Sleeping : "+time_formatted_condensed)
	exit(3)

# if the code has reached this far, 
# then there is a task to be done,
# and there isn't another task running

print("Taking On New Task : "+time_formatted_condensed)

task_to_run = task_bin[0]

# parseXML -> (name, script, inputs)
name, script, inputs = run_task.parseXML(task_to_run)	

# output folder name
output_folder_name = "task-"+str(uuid.uuid1()) 

output_folder = "/var/www/html/output/"+output_folder_name

output_file = output_folder+"/"+name+".out"

#if not os.isdir(output_folder):
cmd_for_dir = "mkdir "+output_folder

cmd_to_run = "python3 "+script+" "+task_to_run+" > \""+output_file+"\""

cmd_to_move_task = "mv \"/root/task_bin/"+task_to_run+"\" \"/var/www/html/output/"+output_folder_name+"/task.xml\""

# add flag
os.system(create_flag)

# makes output/name
os.system(cmd_for_dir)

# runs command
if script is None:
	print("Task has no script")
else:
	os.system(cmd_to_run)

# moves task to bin as well
os.system(cmd_to_move_task)

# remove sys flag
os.system(remove_flag)

