"""


@author: Keith Allatt


"""

import xml.etree.ElementTree as ET
import ast

import sys
sys.path.insert(0, "/root/scripts/dependencies")


import os


def type_conversion(dtype, value):
	"""
	Convert values from a string into a python type
	"""
	if value == "None":
		return None

	if dtype.startswith("int"):
		if dtype == "int":
			return int(value)
		else:
			# ex: "int16" "ff" -> 255
			return int(value, int(dtype[3:]))
	if dtype == "float":
		return float(value)
	
	if dtype == "boolean":
		return value.lower()=="true"
	
	if dtype == "list":
		return ast.literal_eval(value)
	
	# nothing else to do
	return value


def parseXML(in_xml):
	tree = ET.parse('/root/task_bin/'+in_xml)
	root = tree.getroot()

	name   = None
	script = None
	inputs = None

	name = root.attrib.get("name", None)


	for child in root:
		if script is None and child.tag == 'script':
			script = child.attrib.get("name", None)
		if inputs is None and child.tag == 'input_list':
			inputs = []
			for input_line in child:
				if input_line.tag == 'input':
					t = input_line.attrib.get('type', None)
					v = input_line.attrib.get('value', None)
					inputs.append(type_conversion(t, v))
	if script is not None:
		script = "/root/scripts/"+script	
	
	# remove task name spaces
	name = name.replace(" ", "")

	return (name, script, inputs)
	

