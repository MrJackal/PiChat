import socket
import sys
import time
import threading
import json
import requests

SERVER_HOST = '127.0.0.1'
SERVER_API_URL = "http://" + SERVER_HOST + "/api"
SERVER_PORT = 12347
BUFFER_SIZE = 1024
running = True

s = ""
Username = ""
_cmdprefix = "!"

_helpcommands = {}
_commands = {}


def gethelpcommandlist():
    r = requests.get(SERVER_API_URL+"/commands/help")
    return json.loads(r.text)


def getcommandlist():
    r = requests.get(SERVER_API_URL+"/commands/all")
    return json.loads(r.text)


def client(conn):
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break

        response_data = json.loads(data)
        if response_data["cmd"] == "recv_message":
            print(response_data["data"]["username"] + ": " + response_data["data"]["message"])

        if response_data["cmd"] == "recv_connection":
            print(response_data["data"]["username"] + " has joined.")


def get_help():
    print "----- Displaying Results for Help -----\n"
    for command in _commands:
        printed = 0
        for command_details in command:
            if printed == 0:
                print command["name"] + ":- " + command["desc"] + " Usage: " + command["usage"] + "\n"
                printed = 1
    print "----- End Results for Help -----\n"


def send_userconnect(sock, username):
    send_connection = {'cmd': 'user_connect', 'data': {'username': username}}
    sock.send(json.dumps(send_connection))


def sendmessage(sock):
    while True:
        MESSAGE = (raw_input())
        if MESSAGE == "!exit":
            sock.close()
            raise SystemExit
        if MESSAGE == _cmdprefix + "help":
            get_help()

        message_data = {'cmd': 'send_message', 'data': {'username': Username, 'message': MESSAGE}}

        sock.send(json.dumps(message_data))


while running:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting...")
        s.connect((SERVER_HOST, SERVER_PORT))

        Username = (raw_input("Username: "))

        send_userconnect(s, Username)

        print("Grabbing All the Required Information...")
        _helpcommands = gethelpcommandlist()
        _commands = getcommandlist()
        print("Done...")

        # Store thread for receiving from server
        threading.Thread(target=client, args=(s,)).start()

        # Store thread for sending messages
        threading.Thread(target=sendmessage, args=(s,)).start()

        running = False
        time.sleep(20)
    except Exception as e:
        print(e)
        time.sleep(1)
