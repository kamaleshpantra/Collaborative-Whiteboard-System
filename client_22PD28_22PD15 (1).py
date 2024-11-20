import tkinter as tk
import socket
import threading
import pickle

# Server settings
HOST = '127.0.0.1'
PORT = 5000

class WhiteboardClient:
    def __init__(self, root):
        # Set up the socket connection to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))
        
        # Set up the tkinter window
        self.root = root
        self.root.title("Collaborative Whiteboard")
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        # Mouse events
        self.canvas.bind("<B1-Motion>", self.draw)
        self.last_x, self.last_y = None, None

        # Start the receive thread
        threading.Thread(target=self.receive_data, daemon=True).start()

    def draw(self, event):
        if self.last_x and self.last_y:
            # Draw on local canvas
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill="black", width=2)
            
            # Send data to server
            data = ("line", self.last_x, self.last_y, event.x, event.y, "black")
            self.client_socket.sendall(pickle.dumps(data))

        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def receive_data(self):
        while True:
            try:
                data = pickle.loads(self.client_socket.recv(1024))
                if data[0] == "line":
                    _, x1, y1, x2, y2, color = data
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    root = tk.Tk()
    client = WhiteboardClient(root)
    root.mainloop()
