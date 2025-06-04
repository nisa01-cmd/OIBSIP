import socket
import threading
import tkinter as tk
from tkinter import Toplevel, Button
from tkinter import messagebox
import sqlite3
import emoji

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server():
    try:
        client.connect(('localhost', 12345))
    except:
        messagebox.showerror("Error", "Server not available.")
        return False
    return True

# --- GUI Setup ---
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application - Login")
        self.username = None

        self.login_frame = tk.Frame(root)
        self.chat_frame = tk.Frame(root)

        self.build_login_frame()

    def build_login_frame(self):
        self.login_frame.pack()
        tk.Label(self.login_frame, text="Username").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        tk.Label(self.login_frame, text="Password").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        tk.Button(self.login_frame, text="Login", command=self.login_user).pack(pady=5)
        tk.Button(self.login_frame, text="Register", command=self.register_user).pack()

    def register_user(self):
        uname = self.username_entry.get()
        pwd = self.password_entry.get()
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (uname, pwd))
            conn.commit()
            messagebox.showinfo("Success", "User Registered!")
        except:
            messagebox.showerror("Error", "User already exists!")
        conn.close()

    def login_user(self):
        uname = self.username_entry.get()
        pwd = self.password_entry.get()
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (uname, pwd))
        result = c.fetchone()
        conn.close()

        if result:
            self.username = uname
            if connect_to_server():
                client.send(uname.encode())
                self.login_frame.pack_forget()
                self.build_chat_frame()
                threading.Thread(target=self.receive_msg).start()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    def build_chat_frame(self):
        self.chat_frame.pack()

        self.text_area = tk.Text(self.chat_frame, height=20, width=50)
        self.text_area.pack()
        self.text_area.config(state=tk.DISABLED)

        self.msg_entry = tk.Entry(self.chat_frame, width=40)
        self.msg_entry.pack(side=tk.LEFT)

        tk.Button(self.chat_frame, text="😊", command=self.open_emoji_picker).pack(side=tk.LEFT)   
        tk.Button(self.chat_frame, text="Send", command=self.send_msg).pack(side=tk.LEFT)

    def open_emoji_picker(self):
        emoji_window = Toplevel(self.root)
        emoji_window.title("Choose Emoji")
        emojis = ['😀', '😂', '😍', '😎', '😭', '😡', '👍', '👎', '🙏', '❤️']

        for emo in emojis:
           btn = Button(emoji_window, text=emo, font=("Arial", 14), command=lambda e=emo: self.insert_emoji(e))
           btn.pack(side=tk.LEFT)

    def insert_emoji(self, emoji_char):
        current_text = self.msg_entry.get()
        self.msg_entry.delete(0, tk.END)
        self.msg_entry.insert(0, current_text + emoji_char)


    def send_msg(self):
        msg = self.msg_entry.get()
        if msg:
           # Show own message locally
           self.text_area.config(state=tk.NORMAL)
           self.text_area.insert(tk.END, f"You: {msg}\n")
           self.text_area.config(state=tk.DISABLED)

           # Send to server
           client.send(msg.encode())
           self.msg_entry.delete(0, tk.END)

    def receive_msg(self):
        while True:
            try:
                msg = client.recv(1024).decode()
                self.text_area.config(state=tk.NORMAL)
                self.text_area.insert(tk.END, msg + "\n")
                self.text_area.config(state=tk.DISABLED)
            except:
                break

# --- Launch the App ---
root = tk.Tk()
app = ChatApp(root)
root.mainloop()
