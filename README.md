Environment:
Operating System- Windows
Programming language – Python 3.6
To run – Python 3.6 
Available at: https://www.python.org/downloads/
		(Or)
JetBrains  Pycharm Installer guide: https://www.jetbrains.com/pycharm/

				(download python 3.6)
Note: Refer screen shots folder
Compiling and Running the application:
1.	Start the server
2.	Start the Processes (one at a time)
3.	Server displays the process id of the processes that are connected to the server.
4.	Every process waits for 15 seconds except process 3 (12 seconds). In that waiting time if the process doesn’t receive any message that process start the election.
5.	While performing the election any new process joined the ring, again the election starts in the ring.
6.	Once coordinator for the ring is elected a common token “hello from “+process id is being circulated all along the ring.
Example :1->2->3->1
2 receives “hello from 1”,3 receives “hello from 2” and 1 receives “hello from 1”.

7.	If we manually stop’s coordinator process. a new election is started at all the process which do not receive any message in their default delay time.
8.	If we manually stop’s any process other than coordinator no election is started and the message to the stopped process are redirected to next process.


Assumptions:
1. Every process waits for 15 seconds except process 3 waits for 12 seconds (which is start multiple elections), if the processes don’t receive any message in that time it starts election. Sometimes multiple elections also start’s.
2.Every process is put in sleep for one second before it sends a message to next process in the ring. This is to show proper communication between processes.  

Limitations:
1.	When multiple elections started in the ring. All the election results will be same that means all the processes that starts the election have same coordinator, and all process which starts the election start’s passing the “hello from + process id “token along the ring. Because of that multiple “hello from+ process id “token is passing along the ring.

References:
https://docs.python.org/3/library/socket.html#example
https://www.youtube.com/playlist?list=PLQVvvaa0QuDe8XSftW-RAxdo6OmaeL85M
https://pythonprogramming.net/
http://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method

