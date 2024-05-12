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
    sock.settimeout(1.0)
    sock_con = sock.connect_ex((host, port))
    if sock_con == 0:
        print(str(port)+" is open")
        return sock
    else:
        return None

open_sockets = []
open_ports = []
def port_scan():
    global open_sockets
    global open_ports
    print("auto detecting ports")
    while open_sockets == []:#gonna put some open sockets into a list to cycle through
        for i in range(8000,9000):#auto searches for open sockets between 8000 and 9000
            sock = check_socket(ip_address,i)
            while sock:# if a socket is found on a port, it will try to create as many connections as possible
                open_sockets.append(sock)
                open_ports.append(i)
                print("socket opened, continuing search")
                time.sleep(1)
                sock = check_socket(ip_address,i)
    print("search complete")
#port_scan()

connect = True
current_sock_num = 0

print("""
                 ____                           
     _______  __/ __/_  _______                 
    / ___/ / / / /_/ / / / ___/  ______         
   / /  / /_/ / __/ /_/ (__  )  /_____/         
  /_/   \__,_/_/  \__,_/____/                   
                 ______                         
     _________  / __/ /__      ______ _________ 
    / ___/ __ \/ /_/ __/ | /| / / __ `/ ___/ _ \ 
   (__  ) /_/ / __/ /_ | |/ |/ / /_/ / /  /  __/
  /____/\____/_/  \__/ |__/|__/\__,_/_/   \___/                 


socket testing terminal v2.0
to start, try /scan to try to open up a connection
      
input commands with / and anything else will be encoded and sent
current commands include:
/close to close the socket
/recv to receive data and output it to the command line                  
the /ls command can be used to list current open sockets and in conjunction with the /switch to change active sockets, addressed by their number
the /scan command will scan the ports again to try and establish more connections
the /sendall is for socket_manager modules recvall function
the /connect <port> <ip> allows you to create another connection. if ip is not specified, the local one is use instead""")

if connect:    
    while True:
        try:
            cmd = input(">>>")
            if cmd[0] == "/":
                cmd = cmd[1:].split(" ")
                match cmd[0]:
                    case "close":
                        server.close()
                    case "recv":
                        try:
                            server.settimeout(5.0)
                            print(server.recv(4096))
                        except Exception as problem:
                            print(problem)
                    case "ls":
                        count = 0
                        for i in open_sockets:
                            print("socket number",count,"info:",i.getsockname()[0],i.getsockname()[1])
                            count += 1
                    case "switch":
                        if len(cmd) == 2:
                            selected_socket = int(cmd[1])
                            if 0 <= selected_socket < len(open_sockets):
                                print("switching to",selected_socket)
                                open_sockets[current_sock_num] = server #store the current socket back in open_sockets
                                current_sock_num = selected_socket #update the selectec socket
                                server = open_sockets[selected_socket] #set server to the new current socket
                            else:
                                print("couldnt perform that operation.")
                        else:
                            while True:
                                try:
                                    selected_socket = int(input("select the socket number to switch to:"))
                                    if selected_socket == -1:
                                        break
                                    open_sockets[current_sock_num] = server #store the current socket back in open_sockets
                                    current_sock_num = selected_socket #update the selectec socket
                                    server = open_sockets[selected_socket] #set server to the new current socket
                                    break
                                except:
                                    print("couldnt perform that operation. to cancel input -1")
                    case "scan":
                        port_scan()
                        server = open_sockets[-1]
                    case "sendall":#for the recvall of socket_manager module
                        if len(cmd) == 1:#arguments or not
                            server.sendall((input("enter message >>>")+"\0").encode())
                        else:
                            server.sendall((cmd[1]+"\0").encode())#endstop character
                    case "connect":
                        try:
                            if len(cmd) == 2:
                                connecting_ip = ip_address
                            else: 
                                connecting_ip = cmd[2]
                            connecting_port = cmd[1]
                            new_sock = socket.socket()
                            new_sock.connect((connecting_ip,int(connecting_port)))
                            open_sockets.append(new_sock)
                            print("successfully connected!")
                        except Exception as problem:
                            print(problem)
            else:
                server.sendall(cmd.encode())
        except Exception as problem:
            print(problem)