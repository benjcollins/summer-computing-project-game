from socket import *
from threading import *

QUIT = "%^@"

class Server(Thread):
	
	def __init__(self, port = 9999):
		Thread.__init__(self)
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.host = gethostname()
		self.port = port
		self.running = True
		self.clients = []
		self.onConnect = False
		
	def run(self):
		self.socket.bind((self.host, self.port))
		self.socket.listen(5)
		
		while True:
			
			clientsocket, addr = self.socket.accept()
			
			if not self.running:
				break
			
			client = ClientConnection(clientsocket, addr, self)
			client.start()
			self.clients.append(client)
			if self.onConnect:
				self.onConnect(client)
			
		self.socket.close()
			
	def quit(self):
		self.running = False
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.socket.connect((self.host, self.port))
		self.socket.close()
		
	def send(self, text):
		for client in self.clients:
			client.send(text)
			
	def setOnConnect(self, callback):
		self.onConnect = callback
	
class ClientConnection(Thread):
	
	def __init__(self, socket, addr, server):
		Thread.__init__(self)
		self.socket = socket
		self.addr = addr
		self.onRecv = False
		self.running = True
		self.server = server
		
	def run(self):
		while self.running:
			msg = self.socket.recv(1024)
			text = msg.decode("ascii")
			
			if text == QUIT:
				self.running = False
				self.socket.close()
				i = self.server.clients.index(self)
				self.server.clients.pop(i)
			else:
				if self.onRecv:
					self.onRecv(text)
	
	def send(self, text):
		if self.running:
			msg = text.encode("ascii")
			self.socket.send(msg)
		
	def quit(self):
		self.running = False
		self.send(QUIT)
		self.socket.close()
		i = self.server.clients.index(self)
		self.server.clients.pop(i)
		
	def setOnRecv(self, callback):
		self.onRecv = callback
	
class Client(Thread):
	
	def __init__(self, port = 9999):
		Thread.__init__(self)
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.host = gethostname()
		self.port = port
		self.onRecv = False
		self.running = True
		
	def run(self):
		self.socket.connect((self.host, self.port))

		while self.running:
			msg = self.socket.recv(1024)
			text = msg.decode("ascii")
			
			if text == QUIT:
				self.running = False
				self.socket.close()
			else:
				if self.onRecv:
					self.onRecv(text)
		
	def send(self, text):
		msg = text.encode("ascii")
		self.socket.send(msg)
		
	def quit(self):
		self.running = False
		self.send(QUIT)
		self.socket.close()
		
	def setOnRecv(self, callback):
		self.onRecv = callback