import socket
import threading
import sqlite3

# --- USER DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

init_db()

clients = {}

# --- HANDLE EACH CLIENT ---
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    username = conn.recv(1024).decode()
    clients[username] = conn

    while True:
        try:
            msg = conn.recv(1024).decode()
            if msg:
                print(f"{username}: {msg}")
                # Broadcast
                for user, client_conn in clients.items():
                    if user != username:
                       client_conn.send(f"{username}: {msg}".encode())


        except:
            conn.close()
            del clients[username]
            break

# --- START SERVER ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen()
print("[SERVER STARTED] Listening...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
