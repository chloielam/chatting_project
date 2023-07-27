# build a chat server using socket programming
import socket
import threading

# CLIENT[NICKNAME] = [SOCKET, ADDRESS]
CLIENTS = dict()

# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
port = 9999

# bind to the port
server.bind((host, port))

# listen for clients
server.listen()

# broadcast messages to all clients


def broadcast(message, sender=None):
    for client_socket, address in CLIENTS.values():
        # do not send message to sender
        if client_socket != sender:
            client_socket.send(message)


# handle client messages
def handle(client_socket, nickname):
    while True:
        try:
            # receive message from client
            message = client_socket.recv(1024)
            # broadcast message to all clients
            broadcast(message, client_socket)
        except:
            # remove client from CLIENTS
            del CLIENTS[nickname]
            # broadcast message to all clients
            broadcast(f'{nickname} left the chatroom!'.encode(
                'ascii'))
            break

# handle new connections


def on_connect(client_socket, address):
    # request and store nickname
    nickname = client_socket.recv(1024).decode('ascii')
    while nickname in CLIENTS:
        client_socket.send('RESEND_NICK'.encode('ascii'))
        nickname = client_socket.recv(1024).decode('ascii')
    # store client information
    CLIENTS[nickname] = (client_socket, address)
    # broadcast message to all clients
    broadcast(f'{nickname} joined the chatroom!'.encode(
        'ascii'))
    # start thread for handling client
    thread = threading.Thread(target=handle, args=(client_socket, nickname))
    thread.start()


# start accepting clients
def accept():
    while True:
        client_socket, address = server.accept()
        print(f'Connected with {str(address)}')
        thread = threading.Thread(
            target=on_connect, args=(client_socket, address))
        thread.start()


if __name__ == '__main__':
    print('Server starts listening...')
    accept()
