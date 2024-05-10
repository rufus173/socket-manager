import socket
import time

#use https://harry-pc.duckdns.org to resolve ip
#if not update manualy
ip = "86.160.112.140"

#just setting up variables
hand = []
discard = ""

#we will connect to the server
server = socket.socket()
server.connect((ip,8032))

hand = server.recv(4096).decode().split(",")
print(hand)
server.sendall(b"_")#acknowledgement packet

while True:#mainloop
    response = server.recv(1024).decode()
    match response:
        case "discard":
            server.sendall(b"_")
            discard = server.recv(1024).decode()
            server.sendall(b"_")
        case "go":
            pass #insert code here for your turn