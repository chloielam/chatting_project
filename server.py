import socket
import threading
from sortedcontainers import SortedDict

# CLIENT[NICKNAME] = [SOCKET, ADDRESS]
CLIENTS = SortedDict()

# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow reuse of address

# get local machine name
host = socket.gethostname()
port = 9999


# bind to the port
# allow only one instance of the server to run
try:
    server.bind((host, port))
except:
    exit(0)
# listen for clients
server.listen()

# send welcome message to new client


def welcome(client_socket):
    send_to_client(
        client_socket, ' -----------------------------   Welcome to the chatroom!   ------------------------------\n')
    send_to_client(
        client_socket, ' -------------------------------   Type /help for more info   -------------------------------\n')
    # broadcast('Existing clients: '.encode('utf-8'), "SERVER")
    # for nickname in CLIENTS:
    #     client_socket.send((nickname+" ").encode('utf-8'))

# send private message to a client


def private_message(client_socket, nickname, message):
    message = message.decode('utf-8')
    message = message.split(" ", 2)
    if len(message) < 3:
        client_socket.send(
            '————> Invalid command. Please try again.'.encode('utf-8'))
        return
    if message[1] not in CLIENTS:
        client_socket.send(
            '————> User not found. Please try again.'.encode('utf-8'))
        return
    send_to_client(CLIENTS[message[1]][0],
                   f'[Private from {nickname}]: {message[2]}')


def send_to_client(client_socket, message):
    client_socket.send(message.encode('utf-8'))


# broadcast messages to all clients


def broadcast(message, nickname, sender=None):
    # notification message
    if sender is None:
        # format message to --- message --- that does not exceed 60 characters
        notification = (79-len(message))//2 * '-'  \
            + ' '*6 + message + ' '*6 + (79-len(message))//2 * '-' + '\n'
        notification = notification.encode('utf-8')
        for client_socket, address in CLIENTS.values():
            client_socket.send(notification)
    else:
        for client_socket, address in CLIENTS.values():
            if client_socket is not sender:
                client_socket.send(f'[{nickname}]: '.encode('utf-8') + message)

# handle client messages


def handle(client_socket, nickname):
    while True:
        try:
            # receive message from client
            message = client_socket.recv(1024)
            # private message
            if message.startswith((b'/private')):
                private_message(client_socket, nickname, message)
                continue
            # public message
            broadcast(message, nickname, client_socket)
        except:
            # remove client from CLIENTS
            del CLIENTS[nickname]
            # notify to all clients
            broadcast(f'{nickname} left the chatroom!', "SERVER")
            break


# handle new connections


def on_connect(client_socket, address):
    # request and store nickname
    try:
        nickname = client_socket.recv(1024).decode('utf-8')

        # check if nickname is already taken
        while nickname in CLIENTS:
            client_socket.send(
                'RESEND_NICK'.encode('utf-8'))
            nickname = client_socket.recv(1024).decode('utf-8')

        # store client information
        CLIENTS[nickname] = (client_socket, address)
        # notify to all clients
        broadcast(f'{nickname} joined the chatroom!', "SERVER")
        # welcome new client
        welcome(client_socket)
        # start thread for handling client
        thread = threading.Thread(
            target=handle, args=(client_socket, nickname))
        thread.start()
    except:
        client_socket.close()
        return

# start accepting clients


def accept():
    while True:
        try:
            client_socket, address = server.accept()
            print(f'Connected with {str(address)}')
            thread = threading.Thread(
                target=on_connect, args=(client_socket, address))
            thread.start()
        except:
            break


if __name__ == '__main__':
    import tkinter as tk
    from tkinter import messagebox
    import sys

    root = tk.Tk()

    def on_closing():
        root.destroy()
        server.close()
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Set the window's position
    root.geometry(
        f"{300}x{100}+{(root.winfo_screenwidth() - 300) // 2}+{(root.winfo_screenheight() - 100) // 2}")
    # set the title
    root.title("SERVER IS ONLINE!")

    # display host and port on tkinter windows (centered)
    tk.Label(root, text=f"HOST: {host}").pack(pady=10)
    tk.Label(root, text=f"PORT: {port}").pack(pady=10)

    # start accepting clients
    accept_thread = threading.Thread(target=accept)
    accept_thread.start()
    root.mainloop()
