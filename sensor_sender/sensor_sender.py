'''
This module emulates the sensor readings, which would be sent from the 
Arduino/ESP8266 unit attached to the drone. 

A remote server will listen to, and process the sent readings. 
'''

import socket
import gpiozero

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

def gethitsensor(pin):
    hit_sensor = gpiozero.Button(pin, pull_up=False)
    return hit_sensor.is_pressed()

def getdistance(pin):
    

def getreadings():
    is_hit = gethitsensor(2)
    left_dist = getdistance(5)

def main():
    sock = initsocket()
    
    sendreadings(1.2, 3.4, True, sock)

if __name__ == '__main__':
    main()
    # pass
