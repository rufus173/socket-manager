import socket
from contextlib import closing

#get ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
s.close()


def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            print(str(port)+" is open")
            return port

open_ports = []
print("auto detecting ports")
while open_ports == []:
    for i in range(8000,9000):
        port = check_socket(ip_address,i)
        if port:
            open_ports.append(port)

connect = True
if connect:
    server = socket.socket()
    for port in open_ports:
        if port == None:
            continue #im lazy the function stores the port as none if the port is not open
        try:
            print("attempting to connect to port",port)
            server.connect((ip_address,port))
            print("""socket testing terminal v1.0
                  current commands include /close to close the socket and /recv to receive data and output it to the command line
                  input commands with / and anything else will be encoded and sent""")
            while True:
                cmd = input(">>>")
                if cmd[0] == "/":
                    cmd = cmd[1:]
                    match cmd:
                        case "close":
                            server.close()
                        case "recv":
                            print(server.recv(4096))
                else:
                    server.sendall(cmd.encode())
        except Exception as problem:
            print("error connecting with port",port,problem)
            continue