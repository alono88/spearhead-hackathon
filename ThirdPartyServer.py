import libardrone
import time
import select 
import socket 
import sys

"""
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'at', 'com_pipe', 'com_watchdog_timer', 'commwdg', 'halt', 'hover', 'image', 'ipc_thread', 'land', 'lock', 'move', 'move_backward', 'move_down', 'move_forward', 'move_left', 'move_right', 'move_up', 'nav_pipe', 'navdata', 'network_process', 'reset', 'seq_nr', 'set_speed', 'speed', 'takeoff', 'time', 'timer_t', 'trim', 'turn_left', 'turn_right', 'video_pipe']
"""

SERVER_PORT = 5000
ALL_IPS = '0.0.0.0'
RECV_SIZE = 1024
MAX_HIT_COUNT = 5
MOVE_DOWN_WHEN_HIT_CM = 20 # Moves the drone down when hit by 20 cm
MINIMUM_WALL_PROXIMITY_CM = 20

class ResultEnum():
    WALL, HIT = range(2)

class Drone(object):
    def __init__(self):
        """
        Initialize the drone.
        Moves the drone to the maximal height in its starting point
        """
        self.__current_hit_count = 0
        self.__drone = libardrone.ARDrone()
        self.__drone.takeoff()
        time.sleep(3)
        
        #Testing:
        #import pdb; pdb.set_trace()
        #self.move_drone_forward()
        #self.move_drone_left()
        #self.__drone.land()
        
    def listen_socket(self):
        pass
        backlog = 1
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        s.bind((ALL_IPS, SERVER_PORT)) 
        s.listen(backlog) 
        while True:
            client, address = s.accept() 
            data = client.recv(RECV_SIZE) 
            if data: 
                client.send(data) 
            client.close()

        
    def test(self):
        """
        
        """
        import pdb; pdb.set_trace()
        self.move_drone_left()
        self.__drone.land()
        self.move_drone_left()
        time.sleep(5)
        self.__drone.move_forward()
        time.sleep(1)
        self.__drone.move_backward()
        time.sleep(2)
        self.__drone.land()
        
    def move_drone_left(self):
        """
        Moves the drone left, can only be stopped if the drone has reached the wall or a hit was detected
        """
        self.__drone.move_left()
        pass
        
    def move_drone_right(self):
        """
        Moves the drone right, can only be stopped if the drone has reached the wall or a hit was detected
        """
        self.__drone.move_right()
        pass
        
    def move_drone_forward(self):
        """
        Moves the drone forward, can only be stopped if the drone detected a hit
        """
        self.__drone.move_forward()
        pass
        
    def move_drone_down(self):
        """
        Moves the drone down, can only be stopped if the drone detected a hit
        """
        self.__drone.move_down()
        pass
        
    def move_drone_up(self):
        """
        Moves the drone down, can only be stopped if the drone detected a hit
        """
        self.__drone.move_up()
        pass
        
    def drone_land(self):
        """
        Lands the drone
        """
        self.__drone.land()
        pass
        
    def process_hit(self):
        """
        What to do when the drone was hit
        """
        self.__current_hit_count += 1
        if self.__current_hit_count == MAX_HIT_COUNT:
            self.drone_land()
        else:
            self.move_drone_down()
            time.sleep(1)
        
    def wait_for_interrupt(self):
        """
        Polls the socket and waits for interrupt
        """
        try:
            host = ALL_IPS 
            port = SERVER_PORT
            backlog = 5 
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
            server.bind((host, port)) 
            input = [server] 
            running = 1 
            while running: 
                inputready,outputready,exceptready = select.select(input,[],[]) 
                for s in inputready: 
                    if s == server: 
                        # handle the server socket 
                        data, address = server.recvfrom(RECV_SIZE)
                        try:
                            data = data[:-1].split(",")
                            laser_sensor = data[0]
                            #left_sensor = data[1]
                            #right_sensor = data[2]
                        except:
                            continue
                            
                        if laser_sensor == "1":
                            print "I was hit!"
                            result = ResultEnum.HIT
                            return result
                        #elif float(left_sensor) < MINIMUM_WALL_PROXIMITY_CM:
                        #    result = ResultEnum.WALL
                        #    return result
                        #elif float(right_sensor) < MINIMUM_WALL_PROXIMITY_CM:
                        #    result = ResultEnum.WALL
                        #    return result

        finally:    
            server.close()


def main():
    """
    
    """
    
    drone = Drone()
    #drone.test()
    while True:
        # Move the drone to the left
        #drone.move_drone_left()
        result = drone.wait_for_interrupt()
        if result == ResultEnum.HIT:
            drone.process_hit()
        #elif result == ResultEnum.WALL:
        #    drone.move_forward()
        #    time.sleep(2)
            
        # Move the drone to the right
        #drone.move_drone_right()
        result = drone.wait_for_interrupt()
        if result == ResultEnum.HIT:
            drone.process_hit()
        #elif result == ResultEnum.WALL:
        #    drone.move_forward()
        #    time.sleep(2)

if __name__ == "__main__": 
    main()