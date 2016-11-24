import socket 

SERVER_PORT = 50000
ALL_IPS = '0.0.0.0'
RECV_SIZE = 1024
MAX_HIT_COUNT = 5
MOVE_DOWN_WHEN_HIT_CM = 20 # Moves the drone down when hit by 20 cm

def listen_socket():
    backlog = 5 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((ALL_IPS, SERVER_PORT)) 
    s.listen(backlog) 
    while 1: 
        import pdb; pdb.set_trace()
        client, address = s.accept() 
        data = client.recv(RECV_SIZE) 
        if data: 
            client.send(data) 
        client.close()

def init_drone():
    """
    Initialize the drone.
    Moves the drone to the maximal height in its starting point
    """
    # ...
    move_drone_up()
    # ...
    
    
def move_drone_left():
    """
    Moves the drone left, can only be stopped if the drone has reached the wall or a hit was detected
    """
    pass

def move_drone_right():
    """
    Moves the drone right, can only be stopped if the drone has reached the wall or a hit was detected
    """
    pass
    
def move_drone_forward():
    """
    Moves the drone forward, can only be stopped if the drone detected a hit
    """
    pass
    
def move_drone_down():
    """
    Moves the drone down, can only be stopped if the drone detected a hit
    """
    pass

def move_drone_up():
    """
    Moves the drone down, can only be stopped if the drone detected a hit
    """
    pass
    
def main():
    """
    
    """
    current_hit_count = 0
    init_drone()
    while True:
        # Move the drone to the left
        result = move_drone_left()
        if result.reason == hit
            process_hit()
        elif result.reason == wall:
            result = move_drone_forward()
            
        # Move the drone to the right
        result = move_drone_right()
        if result.reason == hit
            process_hit()
        elif result.reason == wall:
            result = move_drone_forward()
        
    listen_socket()
    
    
if __name__ == "__main__": 
    main()