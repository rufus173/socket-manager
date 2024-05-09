import socket_manager
import threading
import socket
import time

def connect():
    time.sleep(1)
    server = socket.socket()
    server.connect(("192.168.1.239",8033))

server = socket.socket()
handle = socket_manager.handler()
server = handle.auto_bind(8033)
threading.Thread(target=connect).start()
handle.listen(1)