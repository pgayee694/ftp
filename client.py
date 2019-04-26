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
    
def get(fileName, clientSocket):
    if os.path.isfile(fileName):
        answer = input('Current copy of {} already exists. Overwrite? Y/N?\n'.format(fileName)).upper()
        if answer == 'N':
            return
    clientSocket.send('GET {}'.format(fileName).encode())
    line = clientSocket.recv(1024).decode()
    if line == 'Unable to find file {}'.format(fileName):
        print(line)
        return
    f = open(fileName, 'w')
    while line:
        if 'EOF' in line:
            line = line.split('EOF')[0]
            f.write(line)
            break
        f.write(line)
        line = clientSocket.recv(1024).decode()
    f.close()
    print('File acquired\n')

def mkdir(directoryName, clientSocket):
    clientSocket.send('MKDIR {}'.format(directoryName).encode())
    response = clientSocket.recv(1024).decode()
    if response != 'ACK':
        print('Directory already exists. Aborting')
    else:
        print('Directory successfully created')

def chdir(directoryName, clientSocket):
    clientSocket.send('CHDIR {}'.format(directoryName).encode())
    response = clientSocket.recv(1024).decode()
    if response != 'ACK':
        print('Directory does not exist. Aborting')
    else:
        print('Changed to {}'.format(directoryName))

def rmdir(directoryName, clientSocket):
    clientSocket.send('RMDIR {}'.format(directoryName).encode())
    response = clientSocket.recv(1024).decode()
    if response != 'ACK':
        print('Directory does not exist. Aborting')
    else:
        print('Deleted directory {}'.format(directoryName))


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
    elif command == 'GET':
        get(args[1], clientSocket)
    elif command == 'LIST':
        clientSocket.send('LIST'.encode())
        print(clientSocket.recv(1024).decode())
    elif command == 'MKDIR':
        mkdir(args[1], clientSocket)
    elif command == 'CHDIR':
        chdir(args[1], clientSocket)
    elif command == 'RMDIR':
        rmdir(args[1], clientSocket)
    elif command == 'ABORT':
        break