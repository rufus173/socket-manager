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


#card display
def display(hand):
    hand_str = "" #we need to build it 1 line at a time,and ensure colouring and symbols are correct
    top = ""
    mid_top = ""
    mid = ""
    mid_bottom = ""
    bottom = ""
    for card in hand:
        colour = "\033[0m"
        match card[0]: #figure out ansi escape code required
            case "g":
                colour = "\033[32m"
            case "b":
                colour = "\033[34m"
            case "y":
                colour = "\033[33m"
            case "r":
                colour = "\033[31m"
        match card[1]:
            case "r":
                display_card = " ⇅ "
            case "s":
                display_card = " Ø "
            case "t":
                display_card = "+ 2"
            case "f":
                display_card = "+ 4"
            case "n":
                display_card = " w "
            case _:
                display_card = " "+card[1]+" "
        if card[0] != "w":
            top = top + colour + "╔═══════╗" + "\033[0m"
            mid_top = mid_top + colour + "║       ║" + "\033[0m"
            mid = mid + colour + "║  " + display_card + "  ║"
            mid_bottom = mid_bottom + colour + "║       ║" + "\033[0m"
            bottom = bottom + colour + "╚═══════╝" + "\033[0m"
        else:
            top = top + "\033[31m╔═\033[0m═════\033[32m═╗" + "\033[0m"
            mid_top = mid_top + colour + "\033[31m║ \033[0m     \033[32m ║" + "\033[0m"
            mid = mid + colour + "║  " + display_card + "  ║"
            mid_bottom = mid_bottom + colour + "\033[34m║ \033[0m     \033[33m ║" + "\033[0m"
            bottom = bottom + colour + "\033[34m╚═\033[0m═════\033[33m═╝" + "\033[0m"
    hand_str += top + "\n" + mid_top + "\n" + mid + "\n" +  mid_bottom + "\n" + bottom
    print(hand_str)

#just setting up variables
hand = []
discard = ""

#we will connect to the server
server = socket.socket()
server.connect((ip,8032))

hand = server.recv(4096).decode().split(",")
print(hand)
display(hand)
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