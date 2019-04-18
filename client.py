from socket import *
import sys
import os

def stor(fileName, clientSocket):
    try:
        f = open(fileName, 'r')
    except IOError:
        print('Unable to find file, please try again\n')
        return
    clientSocket.send('STOR {}'.format(fileName).encode())
    response = clientSocket.recv(1024).decode()
    if response == 'File already exists. Overwrite? Y/N':
        answer = input('File already exists. Overwrite? Y/N\n').upper()
        clientSocket.send(answer.encode())
        if answer == 'N':
            print('Aborting...')
            return
    line = f.read(1024)
    while line:
        clientSocket.send(line.encode())
        line = f.read(1024)
    f.close()
    clientSocket.send('EOF'.encode())
    success = clientSocket.recv(1024).decode()
    if success != 'ACK':
        print('Error uploading file\n')
    else:
        print('Successfully uploaded {}'.format(fileName))


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
    