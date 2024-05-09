import socket
class handler:
	def __init__(self):
		self.server = socket.socket()
	def auto_bind(self,port):#finds your ip and binds (requires port)
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		ip_address = s.getsockname()[0]
		print("ip address:",ip_address)
		self.server.bind((ip_address,port))
