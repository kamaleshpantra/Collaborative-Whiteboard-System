import socket
import threading
import pickle

# Server settings
HOST = '127.0.0.1'
PORT = 5000

# Store connected clients
clients = []

def broadcast(data):
    """Send data to all connected clients."""
    for client in clients:
        try:
            client.sendall(pickle.dumps(data))
        except:
            clients.remove(client)

def handle_client(client):
    """Handle a single client connection."""
    while True:
        try:
            data = pickle.loads(client.recv(1024))
            if data:
                broadcast(data)
        except:
            clients.remove(client)
            break

def main():
    """Set up the server and handle new connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Server started. Waiting for clients...")

    while True:
        client, addr = server.accept()
        print(f"Client {addr} connected.")
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    main()
