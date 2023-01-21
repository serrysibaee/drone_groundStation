
# making abstract class for udp server 
import socket

class Client:
    def __init__(self) -> None:
        self.host = "127.0.0.1"
        self.port = 4455

    def start_server(self):

        self.addr = (self.host, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send(self, mess:str):
        data = mess.encode("utf-8")
        self.client.sendto(data,self.addr)

    def recive(self, addr):
        data, addr = self.client.recvfrom(1024)
        return data.decode("utf-8")