import socket
import sys
import time
import threading
import json
import requests

TCP_IP = '127.0.0.1'
apiURL = "/api"
TCP_PORT = 12346
BUFFER_SIZE = 1024
running = True

s = ""
Username = ""
_cmdprefix = "!"

_helpcommands = {
    "help": {
        "desc": "A list of all commands.",
        "cli_cmd": "get_help"
    }
}

_commands = {
    "list": {
        "name": "list",
        "desc": "Will return all online users.",
        "usage": "!list",
        "srv_cmd": "get_userlist"
    },
    "quit": {
        "name": "quit",
        "desc": "This will disconnect your from the server.",
        "usage": "!quit",
        "srv_cmd": "user_disconnect"
    },
    "msg": {
        "name": "msg",
        "desc": "Send a private message to the specified person",
        "usage": "!msg [user]",
        "srv_cmd": "send_privatemessage"
    },
    "ban": {
        "name": "ban",
        "desc": "Ban the specified person from the server or Ban them for a certain time e.g. 1m, 3h, 4d, 5w, 6M, 7Y.",
        "usage": "!ban [user] {time}",
        "srv_cmd": "user_ban"
    },
    "kick": {
        "name": "kick",
        "desc": "Kick the specified person from the server.",
        "usage": "!kick [user]",
        "srv_cmd": "user_kick"
    },
    "mute": {
        "name": "mute",
        "desc": "Mute the specified person or Mute then for a certain time e.g. 1m, 3h, 4d, 5w, 6M, 7Y.",
        "usage": "!mute [user] {time}",
        "srv_cmd": "user_mute"
    }
}


def gethelpcommandlist():
    r = requests.get(TCP_IP+apiURL+"/commands/help")
    if r.status_code == 200:
        _commands = r.json()


def getcommandlist():
    r = requests.get(TCP_IP+apiURL+"/commands/all")
    if r.status_code == 200:
        _commands = r.json()


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
    for command in _commands.values():
        printed = 0
        for command_details in command.keys():
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
        s.connect((TCP_IP, TCP_PORT))

        Username = (raw_input("Username: "))
        print(Username + " has joined")

        send_userconnect(s, Username)

        # Store thread for receiving from server
        threading.Thread(target=client, args=(s,)).start()

        # Store thread for sending messages
        threading.Thread(target=sendmessage, args=(s,)).start()

        running = False
        time.sleep(20)
    except Exception as e:
        print(e)
        time.sleep(1)
