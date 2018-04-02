import socket                                         
import pickle
from struct import unpack, pack
import threading
import time
import sys
from networking import generic_send_loop, generic_listen_loop
import update
import mp
from update import output

class Server:
    def __init__(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.host = socket.gethostname()                           
        self.port = 9999                                           
        self.serversocket.bind((self.host, self.port))     
        self.clientsocket = None

    def listen(self):
        threading.Thread(target = self.listen_loop, args = []).start()

    def send(self):
        threading.Thread(target = self.send_loop, args = []).start()
        
    def send_loop(self):
        while True:
            if self.clientsocket is not None:
                output("locks", "acquiring outgoing lock")

                with mp.outgoing_lock:
                    for data in mp.outgoing_commands:
                        generic_send_loop(data, self.clientsocket)
                        mp.outgoing_commands.remove(data)

                output("locks", "releasing outgoing lock")
            # time.sleep(1)

    def listen_loop(self):
        self.serversocket.listen(5)
        self.clientsocket,address = self.serversocket.accept()  
        clientsocket = self.clientsocket
        
        size = None 
        data = b''
        
        while True:

            mp.incoming_commands, data, size = generic_listen_loop(clientsocket, mp.incoming_commands, data, size)
            # time.sleep(1)

