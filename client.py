import socket
import threading

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
port = 9999

# connect to the server
client.connect((host, port))


# receive messages from server
def receive():
    while True:
        message = client.recv(1024).decode('ascii')
        print(message)


# send messages to server
def write(nickname):
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


# request and store nickname
nickname = input('Choose your nickname: ')
client.send(nickname.encode('ascii'))
message = client.recv(1024).decode('ascii')
while message == 'RESEND_NICK':
    nickname = input('Nickname already in use. Choose another: ')
    client.send(nickname.encode('ascii'))
    message = client.recv(1024).decode('ascii')


# start threads for listening and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write, args=(nickname,))
write_thread.start()
