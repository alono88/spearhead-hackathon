'''
This module emulates the sensor readings, which would be sent from the 
Arduino/ESP8266 unit attached to the drone. 

A remote server will listen to, and process the sent readings. 
'''

import socket
import time

SERVER_PORT = 50000
SERVER_IP = "10.26.108.202"

def initsocket():
    '''
    Initializes and returns a UDP socket. 
    '''
    return socket.socket(
        socket.AF_INET, # Internet
        socket.SOCK_DGRAM) # UDP

def senddata(data, sock):
    '''
    Sends a data string using an open socket. 
    '''
    
    sock.sendto(data, (SERVER_IP, SERVER_PORT))

def gensensorpacket(left_dist, right_dist, is_hit):
    '''
    Generates a data packet to be sent to the remote server. 
    '''
    data = {
            'left_dist': left_dist, 
            'right_dist': right_dist, 
            'is_hit': is_hit,
        }
    
    return '{is_hit:d},{left_dist},{right_dist}'.format(**data)

def sendreadings(left_dist, right_dist, is_hit, sock):
    '''
    Sends the current sensor readings to the remote server. 
    
    @param left_dist: The measured distance (in centimeters) to the left. 
    @type left_dist: float
    @param right_dist: The measured distance (in centimeters) to the right. 
    @type right_dist: float
    @param is_hit: Indicates whether the drone has been hit. 
    @type is_hit: bool
    
    @returns: None
    '''
    data_str = gensensorpacket(left_dist, right_dist, is_hit)
    senddata(data_str, sock)

# The following defines a list of simulated hits. 
# Ordered by ascending row index, 
# the list tells at which row, and at what index to simulate a hit. 
HIT_LIST = [
    (0, 0.7), 
    (2, 0.3), 
    (3, 0.5), 
    (5, 0)
    ]

# How many rows will the drone go through before beating the player:
ROW_COUNT = 5

DISTANCE_THRESHOLD = 20

def runsandbox():
    # Emulates the sensor readings for a game.
    sock = initsocket()
    for i in xrange(ROW_COUNT):
        for j in xrange(0.5 if i == 1 else 0, 1, 0.1):
            if (i, j) in HIT_LIST:
                is_hit = True
            else:
                is_hit = False
            
            sendreadings(
                DISTANCE_THRESHOLD + 10, 
                DISTANCE_THRESHOLD + 10, 
                is_hit, 
                sock)
            
            time.sleep(1)
        
        sendreadings(
            DISTANCE_THRESHOLD / 2, 
            DISTANCE_THRESHOLD / 2, 
            False, 
            sock)
        
        time.sleep(1)

def main():
    
    # sock = initsocket()
    
    # sendreadings(1.2, 3.4, True, sock)
    runsandbox()

if __name__ == '__main__':
    main()
    # pass
