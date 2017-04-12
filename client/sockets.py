import socket
import sys
import time
import traceback
import json

TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024
running = True


while running == True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting...")
        s.connect((TCP_IP,TCP_PORT))
        Username = (raw_input("Username: "))
        print("Connected!")
        while True:
            MESSAGE = (raw_input("Message: "))
            if MESSAGE == "exit":
                s.close()
                raise SystemExit
            message_data = {'username': Username, 'message': MESSAGE}

            s.send(json.dumps(message_data))
            data = s.recv(BUFFER_SIZE)

            response_data = json.loads(data)

            print(response_data.username + ": " + response_data.message)

        running = False
        time.sleep(20)
    except Exception as e:
        print(e)
        time.sleep(1)