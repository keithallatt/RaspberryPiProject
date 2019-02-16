"""

@author: Keith Allatt


"""

import sys
import time

format = "%a, %d %b %Y, %Z, %H:%M:%S"

time_run = time.strftime(format)


args = sys.argv[1:]


def __set_args__(arg_list = sys.argv[1:]):
	"""
	Set the system arguments, for when 
	code is not activated from the command 
	line, but rather from the task scheduler.
	
	:param arg_list: the argument list to 
			 set as the system arguments.
	"""
	global args
	args = arg_list

def __get_args__():
	"""
	Get the arguments currently stored
	as the system arguments.

	:return: system arguments.
	"""
	global args
	return args

def __get_time_run__():
	"""
	Get the time this code was run. Runs
	when this file is loaded as a dependency.

	Alternatively, the first line in a dependant
	file could run @__get_time_now__() to capture
	the time the file was run.

	:return: the time this file was loaded and run.
	"""
	global time_run
	return time_run

def __get_time_now__():
	"""
	Get the time as of this moment. Can be used en 
	lieu of @__get_time_run__() to capture the time
	this file was loaded.

	:return: the current time.
	"""
	return time.strftime(format)

if __name__ == "__main__":
	print(__get_time_now__())

