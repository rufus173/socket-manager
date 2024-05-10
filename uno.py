import socket
import socket_manager
import random

#lets build the deck
#we shall use the notation colour card, e.g r0 for red skip and gs for green skip
deck = ["r0","g0","b0","y0"] #we can use w for wild , e.g. w0 for wild card and w4 for wild +4. for plus 2 we can use colour + p, e.g. gp for green +2
for i in range(2):
    for c in ["r","g","b","y"]:
        for n in range(9):
            deck.append(c+str(n+1))
        for s in ["s","r","p"]:
            deck.append(c+s)
for i in range(4):
    deck.append("w0")
    deck.append("w4")
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
random.shuffle(deck)
hands = {}

for i in range(pcount):
    hands[i] = []
    for j in range(7):
        hands[i].append(deck.pop(0))

print(hands)

for i in range(pcount):
    handle.sockets[i].recv(1024)
    temp = ""
    for c in hands[i]:
        temp = temp + c + ","
    temp = temp.rstrip(",")
    handle.sockets[i].sendall(temp.encode())
    handle.sockets[i].recv(1024)