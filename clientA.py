import socket
import time


host = '127.0.0.1'
port = 8888
BUFFER_SIZE = 2000
MESSAGE = input(" -> ")

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))

tcpClientA.send(MESSAGE.encode())
while MESSAGE != 'exit':
    data = tcpClientA.recv(BUFFER_SIZE)

    print("Client2 received data: ", data.decode())
    
    MESSAGE =  input(" -> ")
    tcpClientA.send(MESSAGE.encode())

time.sleep(2)