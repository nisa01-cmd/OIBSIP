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

# --- BROADCAST FUNCTION ---
def broadcast(message, sender_username):
    for user, client_conn in clients.items():
        if user != sender_username:
            try:
                client_conn.send(message.encode('utf-8'))
            except:
                client_conn.close()
                del clients[user]

# --- HANDLE EACH CLIENT ---
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        username = conn.recv(1024).decode('utf-8')
        clients[username] = conn
        print(f"[USER JOINED] {username}")

        while True:
            msg = conn.recv(1024).decode('utf-8')
            if msg:
                print(f"{username}: {msg}")
                broadcast(f"{username}: {msg}", sender_username=username)
            else:
                break
    except Exception as e:
        print(f"[ERROR] {addr} - {e}")
    finally:
        conn.close()
        if username in clients:
            del clients[username]
        print(f"[DISCONNECTED] {username}")

# --- START SERVER ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen()
print("[SERVER STARTED] Listening on port 12345...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
    thread.start()
