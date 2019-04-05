from socket import *
import sys

def stor(fileName, clientSocket):
    clientSocket.send('STOR {}'.format(fileName).encode())
    f = open(fileName, 'r')
    line = f.read(1024)
    while line:
        clientSocket.send(line.encode())
        line = f.read(1024)
    f.close()
    clientSocket.send('fin'.encode())
    success = clientSocket.recv(1024).decode()
    if success != 'File successfully uploaded':
        print('Error uploading file\n')


serverName = 'localhost'
serverPort = 21
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
while True:
    inpt = input('Please enter your command:\n')
    args = inpt.split()
    command = args[0]
    if command == 'STOR':
        stor(args[1], clientSocket)
    