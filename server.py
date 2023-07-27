# build a chat server using socket programming
import socket
import threading

# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
port = 9999

# bind to the port
server.bind((host, port))

# queue up to 5 requests
server.listen(5)

# list of clients
clients = []

# list of nicknames
nicknames = []

# broadcast message to all clients
def broadcast(message,sender=None):
    for client in clients:
        if client != sender:
            client.send(message)
    print(message.decode('ascii'))
# handle messages from clients
def handle(client):
    while True:
        try:
            # broadcast message
            message = client.recv(1024)
            broadcast(message,client)
        except:
            # remove and close client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break
# receive and broadcast messages
def receive():
    while True:
        # accept connection
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        # request and store nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # print and broadcast nickname
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!\n'.encode('ascii'))
        # start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
receive()




