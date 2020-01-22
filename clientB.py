import socket 
import time

host = '127.0.0.1'
port = 8888
BUFFER_SIZE = 2000
MESSAGE = input(" -> ")

tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientB.connect((host, port))

tcpClientB.send(MESSAGE.encode())
while MESSAGE != 'exit':
    data = tcpClientB.recv(BUFFER_SIZE)

    print("Client2 received data: ", data.decode())
        
    MESSAGE =  input(" -> ")
    tcpClientB.send(MESSAGE.encode())

time.sleep(2)