print("""                 ____                           
     _______  __/ __/_  _______                 
    / ___/ / / / /_/ / / / ___/  ______         
   / /  / /_/ / __/ /_/ (__  )  /_____/         
  /_/   \__,_/_/  \__,_/____/                   
                 ______                         
     _________  / __/ /__      ______ _________ 
    / ___/ __ \/ /_/ __/ | /| / / __ `/ ___/ _ \ 
   (__  ) /_/ / __/ /_ | |/ |/ / /_/ / /  /  __/
  /____/\____/_/  \__/ |__/|__/\__,_/_/   \___/

    V1.1 | uno client for multiplayer uno      """)         


import socket
import time

#use https://harry-pc.duckdns.org to resolve ip
#if not update manualy
ip = "86.160.112.140"

#purely for testing graphics
print("""\033[31m╔═══════╗
║       ║
║   ⇅   ║
║       ║
╚═══════╝\033[0m""")



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
            print("receiving discard")
            server.sendall(b"_")
            discard = server.recv(1024).decode()
            server.sendall(b"_")
            print(discard)
        case "go":
            print("your turn")
            server.sendall(b"_")#acknowledgement

            #we recieve an updated hand
            hand = server.recv(4096).decode().split(",")
            print(hand)
            
            #insert code for logic of playing cards
            chosen_card = input("card >>>")

            if True:#add logic for wether to draw or play
                server.sendall(b"card")#tell the server we are playing a card
                server.recv(1024)
                server.sendall(chosen_card.encode())
            else:
                server.sendall(b"draw")
                hand.append(server.recv(1024).decode())