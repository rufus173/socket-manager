import socket
from contextlib import closing
import time

#get ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
s.close()


def check_socket(host, port):
    sock = socket.socket()
    sock_con = sock.connect_ex((host, port))
    if sock_con == 0:
        print(str(port)+" is open")
        return sock

open_sockets = []
print("auto detecting ports")
while open_sockets == []:#gonna put some open sockets into a list to cycle through
    for i in range(8000,9000):
        sock = check_socket(ip_address,i)
        if sock:
            open_sockets.append(sock)

connect = True
if connect:
    for server in open_sockets:
        try:
            print("""socket testing terminal v1.0
                  current commands include /close to close the socket and /recv to receive data and output it to the command line
                  input commands with / and anything else will be encoded and sent
                  
                  the /ls command can be used to list current open sockets and in conjunction with the /switch to change active sockets, addressed by their number""")
            while True:
                cmd = input(">>>")
                if cmd[0] == "/":
                    cmd = cmd[1:]
                    match cmd:
                        case "close":
                            server.close()
                        case "recv":
                            print(server.recv(4096))
                        case "ls":
                            count = 0
                            for i in open_sockets:
                                print("socket number",count,"info:",i.getsockname()[0],i.getsockname()[1])
                                count += 1
                        case "switch":
                            while True:
                                try:
                                    selected_socket = int(input("select the socket number to switch to:"))
                                    if selected_socket == -1:
                                        break
                                    server = open_sockets[selected_socket]
                                    break
                                except:
                                    print("couldnt perform that operation. to cancel input -1")
                else:
                    server.sendall(cmd.encode())
        except Exception as problem:
            print("error connecting with port",server.getsockname()[1],problem)
            continue