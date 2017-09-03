# -*- coding: utf-8 -*-
"""
@author: harikrishna,bathala
ID :1001415489
"""

# -*- coding: utf-8 -*-
import socket
import threading
import time
import select
"""Socket object s is created"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""host name is retrieved using gethostname"""
host = socket.gethostname()
"""connected to the port 7777,from which server is listening """
to_port = 7777
s.connect((host, to_port))
"""intializing the current process id to 0 """
my_id = "6"
"""sending the process id to server """
s.send(my_id.encode('utf-8'))
"""Intializing the leader variable ,which is the coordinator of the ring,to -1."""
leader="-1"

"""intiate_election function is used to start the election in the ring,whenever an election is required to elect the coordinator
the ring."""
def initiate_election(s):
    """""putting the current thred to sleep in order to provide delay in the algorithm"""""
    time.sleep(1)
    """"sending the current process id as token """
    s.send(my_id.encode('utf-8'))
    """printing the token sent and displaying the Election intiated message """
    print("token sent: " + my_id)
    print("Election initiated")
"""Ring_Election_Algorithm ,where the actual algorithm is implemented and once the coordinator is initiated a token is passed alomg the ring."""
def Ring_Election_Algorithm(s):

    while True:
        global leader
        try:
            """"setting the timeout to 15 seconds, which is to wait for othe process in ring to send within 15 seconds of time.
            if no message is recieved in that time throws an exception."""
            s.settimeout(15)
            received = s.recv(1024)
            s.settimeout(None)
            """decoding the received message and storing the message in received_token_list """
            received_token_list = received.decode('utf-8')
        #here the timeout exceptiion catches and iniate election
        except socket.timeout:
            leader = "0"
            initiate_election(s)
            continue

        """if current process id is in the received in the message and also it does not have any information about 
         coordinator and also not the common token hello,then the election is started by the current process.
         so, the current checks the received_token_list and elects the maximum token form thel list as coordinator
         and sends the message to next process in the ring"""
        if my_id in received_token_list and "Coordinator: " not in received_token_list and "hello" not in received_token_list:
            """finding the maximum token to elect the leader from the received_token_list"""
            leader = max(received_token_list)
            forwarding_leader = "Coordinator: " + leader
            """""putting the current thred to sleep in order to provide delay in the algorithm"""""
            time.sleep(1)
            """forwarding who is the  coordinator in the ring to the next process in the ring."""
            s.send(forwarding_leader.encode('utf-8'))
            """
        If current process id is not in recevied message that means some on else has started the election
        and cordinator and hello message is not in the received message  ,so the current process adds 
        its process id to the received token list and sends it to the next process"""
        elif my_id not in received_token_list and "Coordinator: " not in received_token_list and "hello" not in received_token_list :

            print("rec tok: " + received_token_list)
            """""leader variablle is set to 0 as it some on eelse in the ring started the election,which coordinator may change"""""
            leader = "0"
            """adding the current process id to the received token list """
            received_token_list = received_token_list + " " + my_id
            """""putting the current thred to sleep in order to provide delay in the algorithm"""""
            time.sleep(1)
            """forwarding the new token list to the next process in the ring"""
            s.send(received_token_list.encode('utf-8'))
            print("adding token: " + received_token_list)
            """ If leader variable is set to -1 and it receives some message it means that the current process does not 
            who is coordinator and it starts the election right away"""
        elif ("hello" in received_token_list or "Coordinator: " in received_token_list )and leader=="-1"  :
                leader="0"
                initiate_election(s)

                """If coordinator is in received message and that lesder which the current process in=s not means that
                new coordinator is been elected and leader variable is updated to the coordinator
                and that message is passed along the next process in the ring.
            """
        elif "Coordinator: " in received_token_list and leader not in received_token_list :
            print(received_token_list)
            """splitting the recevied  message to retrieve who is coordinator and saving it in leader variable"""
            le=received_token_list.split()
            leader=le[1]
            """""putting the current thred to sleep in order to provide delay in the algorithm"""""
            time.sleep(1)
            """passing the message to the next process along the ring."""
            s.send(received_token_list.encode('utf-8'))

            """If every thing above fails that means the cordinator has been elected and common token is passing along the ring.
            so passing that token to next process along the ring.            """
        else :
            if leader=="-1" or leader=="0":
                continue
            else :
                #print("coordinator mm :" + leader)
                print(received_token_list)
                """Adding the current process id to the common token to show to next processs in the ring it is coming from which process. """
                communicate = "hello" + " from " + my_id
                """""putting the current thred to sleep in order to provide delay in the algorithm"""""
                time.sleep(1)
                """passing the message to the next process along the ring."""
                s.send(communicate.encode('utf-8'))
                continue
"""Creating a thread to implement the ring election algorithm and the tarfet function is Ring_Election_Algorithm and
 passing the socket oblect"""

recv_thread = threading.Thread(target=Ring_Election_Algorithm, args=(s,))
recv_thread.start()
recv_thread.join()
s.close()