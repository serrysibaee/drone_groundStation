from UDPclient import Client
import json
from datetime import datetime


class GroundCntrolStation:
        
    def __init__(self) -> None:
        self.client = Client()
        self.counter = 0
        self.message = {"header":{"sys_id":0,"seq number":0,"date_time":str(datetime.now())}, "payload":[0,0]}
    #client.start_server()

    def arm(self):
        pass

    def menu(self):
        print("choose number: \n 1- takeoff \n 2- land \n 3- arm \n 4- disarm \n 5- goto ")

    def send(self,mess):
        self.client.send(mess)
        self.counter += 1
        self.message["header"]["seq number"] = self.counter
        # if number == 1:
        #     self.message["payload"][0] = number
        #     self.message["payload"][1] = alt
        #     mess = json.dumps(self.message)
        #     self.client.send(mess)
        #     #print("done sending take off")
        # # elif number == 2:
        # #     self.message["payload"][0] = number
        # #     mess = json.dumps(self.message)
        # #     self.client.send(mess)

        # # elif number == 3: # arm 
        # else: # all other cases exept goto 
        #     self.message["payload"][0] = number
        #     mess = json.dumps(self.message)
        #     self.client.send(mess)

    def land(self):
        self.message["payload"][0] = 2
        
        mess = json.dumps(self.message)
        self.send(mess)

    def takeoff(self,alt):
        self.message["payload"][0] = 1
        self.message["payload"][1] = alt
        mess = json.dumps(self.message)
        self.send(mess)

    def arm(self):
        self.message["payload"][0] = 3
        mess = json.dumps(self.message)
        self.send(mess)

    def diss_arm(self):
        self.message["payload"][0] = 4
        mess = json.dumps(self.message)
        self.send(mess)

    def goto(self,location = 0):
        self.message["payload"][0] = 5
        mess = json.dumps(self.message)
        self.send(mess)
        

    
    
    
if __name__ == "__main__":
    g_station = GroundCntrolStation()
    print("starting client")
    g_station.client.start_server()
    while True:
        print("start client")
        g_station.menu()
        choice = int(input())
        if choice == 1:
            print("send take off")
            g_station.takeoff(20)
        elif choice == 2:
            print("landing")
            g_station.land()

        elif choice == 3:
            print("arm")
            g_station.arm()

        elif choice == 4:
            print("dis arming")
            g_station.diss_arm()

        elif choice == 5:
            print("goto working ")
            g_station.goto()

        #client.send(message)
        
        data = g_station.client.recive(g_station.client.addr)

        print(data)


