import socket
import time
import sys
import threading
import json

from clients import ChatClient


TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024

CLIENTS = {}

_clientList = []


def client(conn):
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        # broadcast
        # for client in CLIENTS:
        #    client.send(data)
        _userdata = {}
        for chatClient in _clientList:
            _userdata = json.loads(data)
            print(_userdata)
            chatClient.conn.send(data)

        print "[INFO] %s: %s" % (_userdata.username, _userdata.message)
    # the connection is closed: unregister
    del CLIENTS[conn.fileno()]


def listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        # register client
        CLIENTS[conn.fileno()] = conn
        _clientList.append(ChatClient(conn,"",1))
        threading.Thread(target=client, args=(conn,)).start()

if __name__ == '__main__':
    listener()
