from threading import Thread
import time
import sys
import fileinput
from socket import *

# processRequest is the thread code
# - pass the connection object here
def processRequests(connectionSockets, addr):
	while True:
		message = connectionSocket.recv(1024).decode()
		args = message.split()
		command = args[0]
		if command == 'STOR':
			stor(args[1], connectionSocket)
		else:
			connectionSocket.send('Invalid command'.encode())


def stor(fileName, connectionSocket):
	print('here')
	f = open(fileName, 'w')
	line = connectionSocket.recv(1024).decode()
	while line:
		f.write(line)
		line = connectionSocket.recv(1024).decode()
		if line == 'fin':
			break
	f.close()
	connectionSocket.send('File succesfully uploaded'.encode())


# main execution follows:
serverPort = 21
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
	print('Ready to serve...')
	connectionSocket, addr = serverSocket.accept()

	# this is how a thread is created and started
	t = Thread(target=processRequests, args=(connectionSocket, addr))
	t.start()

