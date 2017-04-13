import json
import socket
import threading
import requests

from clients import ChatClient

TCP_IP = '127.0.0.1'
TCP_PORT = 12346
BUFFER_SIZE = 1024


# Description/Message Templates
# <[X]> used to replace with an integer
# <[L]> used to replace with a list of strings/ints/doubles etc

_clientList = []

_validcommands = {
    "help": {},
    "list": {},
    "quit": {},
    "msg": {},
    "ban": {},
    "kick": {},
    "mute": {}
}

_requestcommands = {
    "get_userlist"  # Returns list of users
}


def client(conn):
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break

        _userdata = {}
        for chatClient in _clientList:
            _userdata = json.loads(data)
            username = _userdata["data"]["username"]
            if _userdata["cmd"] == "user_connect":
                msg = {"cmd": "recv_connection", "data": {"username": username}}
                chatClient.conn.send(json.dumps(msg))
                print "[INFO] %s Connected" % (_userdata["data"]["username"])
            if _userdata["cmd"] == "send_message":
                chatClient.conn.send(data)
                print "[INFO] %s: %s" % (_userdata["data"]["username"], _userdata["data"]["message"])

    for index, chatClient in enumerate(_clientList):
        if chatClient.conn.fileno() == conn.fileno:
            del _clientList[index]


def commands(conn):
    while True:
        data = conn


def listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        # register client
        _clientList.append(ChatClient(conn, "", 1))

        # Thread new clients and their sockets
        threading.Thread(target=client, args=(conn,)).start()

        # Thread console commands
        threading.Thread(target=commands, args=(conn,)).start()

    # server closed connection - stop the socket
    s.close()


if __name__ == '__main__':
    listener()
