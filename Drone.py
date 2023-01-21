import asyncio
import socket
import sys
import json
from mavsdk import System
from UDPserver import Server
from datetime import datetime


class Drone:
    def __init__(self) -> None:
        self.counter = 0
        self.sys_id = 1
        self.server_ip     = "127.0.0.1"
        self.server_port   = 20001
        self.MAX_BUFFER_SIZE  = 1024
        self.drone = System()
        self.server = Server()
        self.is_arm = False
        self.is_fly = False
        self.message = {"header":{"sys_id":self.sys_id,"seq number":self.counter,"date_time":str(datetime.now())}, "payload": {"info":[], "heartbeat":[]}}



    async def pre_arm_checks(self):
        """
        General configurations, setups, and connections are done here.
        :return:
        """
        print("Connecting to drone ...")
        await self.drone.connect(system_address="udp://:14540")

        print("Waiting for drone to connect...")
        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print(f"-- Connected to drone!")
                break

        print("Waiting for drone to have a global position estimate...")
        async for health in self.drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("-- Global position estimate OK")
                break

    async def start_drone_connect(self):
        await self.pre_arm_checks()
            

    async def takeoff(self,height):

        print("-- Arming")
        await self.arm()

        print("-- Taking off")
        self.is_fly = True
        await self.drone.action.set_takeoff_altitude(height)
        await self.drone.action.takeoff()

    async def land(self):
        self.is_fly = False
        await self.drone.action.land()

    async def arm(self):
        self.is_arm = True
        await self.drone.action.arm()

    async def dis_arm(self):
        self.is_fly = False
        self.is_arm = False
        await self.drone.action.disarm()

    async def do_move(self,massege):

        mass = json.loads(massege)
        #massege = str.decode(mas)

        if mass["payload"][0] == 1:
            height = mass["payload"][1]
            await self.fly(height)

        elif mass["payload"][0] == 2:
            await self.land()

        elif mass["payload"][0] == 3:
            await self.arm()

        elif mass["payload"][0] == 4:
            await self.dis_arm()

        elif mass["payload"][0] == 5:
            await self.goto()

    async def goto(self,latitude_deg=47.397606, longitude_deg=8.543060):
        async for terrain_info in self.drone.telemetry.home():
            print(terrain_info)
            print (terrain_info.absolute_altitude_m)
            absolute_altitude = terrain_info.absolute_altitude_m
            break
        #47.397606, 8.543060, flying_alt, 0
        print("-- Arming")
        await self.drone.action.arm()

        print("-- Taking off")
        await self.drone.action.takeoff()

        await asyncio.sleep(10)

        # four parameters 
        flying_alt = absolute_altitude + 20.0
        await self.drone.action.goto_location(latitude_deg, longitude_deg, flying_alt, 0)
        await asyncio.sleep(10)

    
    async def fly(self,height):
        await(self.takeoff(height))
        
    async def heartbeat(self):
        battery = "90%"
        sys_name = "best drone name"
        self.message["payload"]["heartbeat"] = [battery,sys_name,"is armed: "+str(self.is_arm),"is flying: "+str(self.is_fly)]

    async def info(self):
        gps = await self.drone.telemetry.get_gps_global_origin()
        agl = await self.drone.action.get_takeoff_altitude()
        asl = await self.drone.action.get_return_to_launch_altitude()
        self.message['payload']["info"] = ["gps: "+str(gps), "agl: "+str(agl), "asl: "+str(asl)]

    async def sec_sender(self):
        pass

    '''
Furthermore, the drone must send the following status messages

● A heartbeat message each 1 sec. The payload must contain the battery level of the
drone. It also has the logical name of drone, and state of the drone (armed, disarmed,
flying, on ground, …)
● An information message that contains
    ○ GPS location of the drone
    ○ Absolute altitude of the drone (ASL)
    ○ Relative altitude of the drone (AGL)
    
    '''

async def main():
    drone = Drone()
    drone.server.start_server()
    await (drone.start_drone_connect())
    while True:
        print("waiting to lesten")
        json_mass, addr = drone.server.recive()
        print(json_mass)
        #print(json_mass["payload"])
        await (drone.do_move(json_mass))
        # asysnc wait 1 sec in the func of heartbeat 
        # in response the heartbeat 
        await drone.info()
        await drone.heartbeat()
        print("\n \n ")
        drone.server.response(str(drone.message),addr)

asyncio.run(main())
        
    
