
This is a project designed to take control of a RPi to schedule, and complete tasks. The way this will be achieved through a scheduling task that will run every specified time interval. When this happens, the script will check for a new task to be run. If there is a new task, it will execute. When the script is executing a task, no other tasks are allowed to run. With enough RPis, using SSH, we should be able to auto distribute tasks (Explained Later)

Each task will consist of some input data, either a single instance or a list, and a given script. In a bin folder (TBA), a given task will be formatted as an xml or other markup language, where parsing is easy. A field labeled 'script' will contain a path to the script to be executed. Each 'input' tagged field will contain a set of data that will be parsed and passed to the script, and the script, input and output will be stored in a row of output, to be checked later.

For low volume tasks, such as home use, 1 to 2 tasks every hour should be enough, unless the input sizes are very large. To accomodate this, the scheduler will have to guage data input size and make appropriate choices as to how to change timing to better accomodate the number of tasks (Idle time should be minimized).

If one given RPi in a pseudo-cluster is loaded with a lot of tasks, that RPi should be able to SSH into another RPi, send the file, verify it was sent correctly (ask the RPi to send the file back, if it matches, then success), and have the other RPi handle the task. This is to cut down on the backlog on any given RPi.


