# -*- coding: utf-8 -*-
"""
@author: harikrishna,bathala
ID :1001415489
"""

# -*- coding: utf-8 -*-

import sys
import threading
import socket

""" host name is retrieved using gethostbyname and  a socket object is created
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
"""host is binded to port to 7777 to listen all incoming requests
"""
port = 7777
try:
    s.bind((host, port))
except socket.error as msg:
    print("bind failed" + str(msg))
    sys.exit()
"""started listening to requests ,upto 10 
"""
s.listen(10)
"""Lists are created to store socket objects and processes ,when ever a new process is connected to server,it's socket object 
is stored in process_sockets_list.process_list is used to store the id of the process.
"""
process_sockets_list = []
process_list = []
neighbor_list = []
msg_token = ""
""" recv_messsage function gets socket object as input parameters and it receives messages from the that process and sends it next process
  along the ring."""
def recv_message(conn):
    while True:
        """ try receiving message from process and if it doesn't it throws the eception which makes it continue
         to receive message"""
        try:
            received = conn.recv(1024)
            msg_token = received.decode('utf-8')
            print("received token: " + msg_token)
        except:
            continue
        """ if the received message has coordinator server stores ."""
        if "Coordinator: " in msg_token :
            le=msg_token.split()
            leader=le[1]
        """storing the index of the process id of the  cordinator."""
        process_index = process_sockets_list.index(conn)
        """  ths is used to know to whom the message is to be redirect if process sending the message is last in list
            then the next process is first process,otherwise the next process.as the processes are communicting in the ring"""
        if len(process_sockets_list)==process_index+1 :
            to_process=0
        else :
            to_process=process_index+1
        """ if the server unable to send the message to next process that means the process is stopped
        this will throws ann exception to remove the process from process_list and also removes the socket object in
        the process_sockets_list and closing that socket connection"""
        try :
            process_sockets_list[to_process].send(received)
            """redirecting the received message to next process in the ring"""
            print("sending :" + received.decode('utf-8'))
            """ if unable to send the message that means the that process is stopped ,so its socket object and
            process id's are remove from respective list."""
        except :
            """if the stopped process is not the coordinator then the message is redirected towards to the next process in the ring"""
            if process_list[to_process]!=leader :
                process_sockets_list[to_process+1].send(received)
                print("sending :" + received.decode('utf-8'))
            """closing the socket object of the stopped process."""
            process_sockets_list[to_process].close()
            """ removing the socket objec from the list"""
            process_sockets_list.remove(process_sockets_list[to_process])
            """removing the process id from proceeses list."""
            process_list.remove(process_list[to_process])
            continue

""" Server listens to all incoming connect requests and accets them and stores their socket object and fork a new thread fro each connection """
while True:
    """try connecting with client if any exception it throws exception """
    try:
        connection, addr = s.accept()
        """appending the new connection's socket and storing it in process_sockets_list """
        process_sockets_list.append(connection)
        """" Now server recieves the clients process_id """
        recv_process_id = connection.recv(1024)
        from_to_process = recv_process_id.decode('utf-8')
        #processes = from_to_process.split()
        """server stores the process id in process_list"""
        process_list.append(from_to_process)
        print("Process: " + from_to_process)
        """once server gets process id of the client server forks a new thread to client
         and to recv_message function and passess the connection oblect"""
        start_thread = threading.Thread(target=recv_message, args=(connection,))
        start_thread.start()
        """catches socket error  if any and dispalys the message."""
    except socket.error as msg:
        print("thread failed"+msg)
"""closing the connection after all operation s are done."""
connection.close()
s.close()

