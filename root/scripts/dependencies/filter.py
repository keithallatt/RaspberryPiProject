"""

Filter files from /root/funnel into task_bin, scripts and left_overs
             +--> *.py  -> /root/scripts
/root/funnel-+--> *.xml -> /root/task_bin
             +--> *.*   -> /root/left_overs

@author: Keith Allatt

"""
import os

folder_to = {
	".py"  : "/root/scripts/",
	".xml" : "/root/task_bin/"
}
left_over =  "/root/left_overs/"
	
for fl in os.listdir("/var/www/html/uploads"):
	extension = fl[(fl.rfind(".") if "." in fl else 0):]	
    
	old_location = "\"/var/www/html/uploads/"+fl+"\""
	fl = fl.replace(" ", "_")
	new_location = "\""+folder_to.get(extension, left_over) + fl + "\""
	
	mv_cmd = " ".join(["mv", old_location, new_location])

	os.system(mv_cmd)
