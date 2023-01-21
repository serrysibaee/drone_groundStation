# making abstract class for udp server 

import socket
import sys



# UDP SERVER 
class Server:
    def __init__(self) -> None:
        self.host = "127.0.0.1"
        self.port = 4455

    # this is init server 
    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # connect here 
        self.server.bind((self.host,self.port))
  
    # this is start_server 
    def recive(self):
        #self.connect() NO reputaion connect 
        data, addr = self.server.recvfrom(1024)
        data = data.decode("utf-8")
        return (data,addr)

    def response(self,mess:str, addr:int):
        data = str.encode(mess,"utf-8")
        self.server.sendto(data, addr)