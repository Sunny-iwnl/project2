import socket

class Client:
	
	def __init__(self, ip):
		self.client = socket.socket()
		self.client.connect((ip, 8008))
	
	def sendAnswer(self, answer):
		client.send(answer)

	def getResponse(self):
		return client.recv(1024)




class Server:
	
	def __init__(self):
		self.server = socket.socket()
		self.server.bind(('0.0.0.0', 8008))
		self.client = None
		sef.cient_address = None
		
	def waitForConnect(self):
		self.server.listen(1)
		(client, client_address) = self.server.accept()
		
	def getResponse(self):
		input = client.recv(1024)
		return input
	
	def sendAnswer(self, answer):
		client.send(answer)
	