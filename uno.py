#                 ____                           
#     _______  __/ __/_  _______                 
#    / ___/ / / / /_/ / / / ___/  ______         
#   / /  / /_/ / __/ /_/ (__  )  /_____/         
#  /_/   \__,_/_/  \__,_/____/                   
#                 ______                         
#     _________  / __/ /__      ______ _________ 
#    / ___/ __ \/ /_/ __/ | /| / / __ `/ ___/ _ \
#   (__  ) /_/ / __/ /_ | |/ |/ / /_/ / /  /  __/
#  /____/\____/_/  \__/ |__/|__/\__,_/_/   \___/                 


import socket
import socket_manager
import random

#lets build the deck
#we shall use the notation colour card, e.g r0 for red zero and gs for green skip
deck = ["r0","g0","b0","y0"] #we can use w for wild , e.g. wn for wild card and wf for wild +4. for plus 2 we can use colour + t, e.g. gp for green +t
#when wildcards are played a colour is selected and they will become colour + type, eg wf(wild +4) becomes gf(green +4)
for i in range(2):
    for c in ["r","g","b","y"]:
        for n in range(9):
            deck.append(c+str(n+1))
        for s in ["s","r","t"]:#skip, reverse, plus 2
            deck.append(c+s)
for i in range(4):
    deck.append("wn")#wild
    deck.append("wf")#wild plus 4
print(deck)

while True: #assume the user is incompetent
    try:
        pcount = int(input("how many players (2+) >>>"))
        if pcount < 2:
            raise ValueError
        break
    except:
        print("please enter a valaid number")

handle = socket_manager.handler()
handle.auto_bind(8032)
handle.listen(pcount)

order = 1 #set to -1 to reverse turn order
turn = 0#whos turn it is
card_stack = 0 #for holding info about stacked +2s and +4s
random.shuffle(deck)
hands = {}

for i in range(pcount):
    hands[i] = []
    for j in range(7):
        hands[i].append(deck.pop(0))

print(hands)

for i in range(pcount):
    temp = ""
    for c in hands[i]:
        temp = temp + c + ","
    temp = temp.rstrip(",")
    handle.sockets[i].sendall(temp.encode())
    handle.sockets[i].recv(1024)

discard = "w"
while discard[0] == "w":#stops the game starting on a wildcard
    discard = deck.pop(0)
print("discard pile",discard)

while True:#the mainloop

    #commands are issued telling the client what to expect, so go for their turn and discard to receive the discard pile

    if turn > pcount-1:#this before check is to allow for skip turns
        turn = 0
    elif turn < 0:
        turn = pcount-1
    turn += order #gonna increment or decrement depending on direction of play
    if turn > pcount-1:
        turn = 0
    elif turn < 0:
        turn = pcount-1
    for i in range(pcount):
        handle.sockets[i].sendall(b"discard")
        handle.sockets[i].recv(1024)
        print("sending discard of",(discard+"\r").encode())
        handle.sockets[i].sendall((discard+"\r").encode())
        handle.sockets[i].recv(1024)

    if not(discard[1] == "f" or discard == "t"):#if they have not been +4d or +2d
        handle.sockets[turn].sendall(b"go")#tell them its their turn
        handle.sockets[turn].recv(1024)
        temp = ""
        for c in hands[turn]:
            temp = temp + c + ","
        temp = temp.rstrip(",")
        handle.sockets[turn].sendall(temp.encode())#resending their hand so i can easily deal with plus 2s and 4s
        response = handle.sockets[turn].recv(1024).decode()#we get their card, or a request to draw 1
        match response:
            case "draw":
                new_card = deck.pop(0)
                hands[turn].append(new_card)
                handle.sockets[turn].sendall(new_card.encode())
            case "card":
                handle.sockets[turn].sendall(b"_")
                discard = handle.sockets[turn].recv(1024).decode()
                hands[turn].remove(discard)#remnove cards from their hand that they play

                #special cards game logic
                if discard[0] == "w":
                    handle.sockets[turn].sendall(b"choose colour")
                    colour = handle.sockets[turn].recv(1024).decode()
                    discard = colour + discard[1]
                    handle.sockets[turn].sendall(b"_")
                else:
                    handle.sockets[turn].sendall(b"no action needed")
                handle.sockets[turn].recv(1024)#acknowledge

                if discard[1] == "r":#reverse
                    order * -1
                    print("reversed turn order to",order)
                if discard[1] == "s":#skip
                    turn += order
                    print("skipped next players turn")
                if discard[1] == "t":# +2
                    card_stack += 2
                    print("added 2 to stack")
                if discard[1] == "f":# +4
                    card_stack += 4
                    print("added 4 to stack")
                # logic neeeded to work out plus 2s and plus 4s and logic for choosing colours
        print("discard pile",discard)
    else:
        handle.sockets[turn].sendall(b"plus")
        print("doing plus card logic")
        handle.sockets[turn].recv(1024)
        temp = ""
        for c in hands[turn]:
            temp = temp + c + ","
        temp = temp.rstrip(",")
        handle.sockets[turn].sendall(temp.encode())#resending their had to update them
        response = handle.sockets[turn].recv(1024).decode()
        if response == "no response":
            print("giving this player the stack of",card_stack)
            for i in range(card_stack):
                hands[turn].append(deck.pop(0))
                temp = ""
                for c in hands[turn]:
                    temp = temp + c + ","
                temp = temp.rstrip(",")
                handle.sockets[turn].sendall(temp.encode())
