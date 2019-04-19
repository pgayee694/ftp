from threading import Thread
import time
import sys
import fileinput
from socket import *
import os

# processRequest is the thread code
# - pass the connection object here
def processRequests(connectionSockets, addr):
	while True:
		message = connectionSocket.recv(1024).decode()
		args = message.split()
		if len(args) == 0:
			command = message
		else:
			command = args[0]
		if command == 'STOR':
			stor(args[1], connectionSocket)
		elif command == 'GET':
			get(args[1], connectionSocket)
		elif command == 'LIST':
			connectionSocket.send(str(os.listdir()).encode())
		else:
			connectionSocket.send('Invalid command'.encode())


def stor(fileName, connectionSocket):
	if os.path.isfile(fileName):
		connectionSocket.send('File already exists. Overwrite? Y/N'.encode())
		answer = connectionSocket.recv(1024).decode()
		if answer == 'N':
			print('Aborting...')
			return
	else:
		connectionSocket.send('Beginning upload'.encode())
	f = open(fileName, 'w')
	line = connectionSocket.recv(1024).decode()
	while line:
		if 'EOF' in line:
			f.write(line.split('EOF')[0])
			break
		f.write(line)
		line = connectionSocket.recv(1024).decode()
	f.close()
	connectionSocket.send('ACK'.encode())

def get(fileName, connectionSocket):
	if os.path.isfile(fileName):
		try:
			f = open(fileName, 'r')
			line = f.read(1024)
			while line:
				connectionSocket.send(line.encode())
				line = f.read(1024)
			connectionSocket.send('EOF'.encode())
			f.close()
		except IOError:
			error = 'Unable to find file {}'.format(fileName)
			connectionSocket.send(error.encode())
	else:
		error = 'Unable to find file {}'.format(fileName)
		connectionSocket.send(error.encode())


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

