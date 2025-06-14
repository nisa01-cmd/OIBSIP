import tkinter as tk
from tkinter import messagebox
import random
import string
import tkinter.messagebox as messagebox

# Function to generate password
def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError

        use_letters = letters_var.get()
        use_digits = digits_var.get()
        use_symbols = symbols_var.get()

        if not (use_letters or use_digits or use_symbols):
            messagebox.showerror("Error", "Select at least one character type!")
            return

        character_set = ''
        if use_letters:
            character_set += string.ascii_letters
        if use_digits:
            character_set += string.digits
        if use_symbols:
            character_set += string.punctuation

        password = ''.join(random.choice(character_set) for _ in range(length))
        result_var.set(password)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive number.")

def copy_to_clipboard():
    password = result_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied!", "Password copied to clipboard.")
    else:
        messagebox.showwarning("No Password", "Please generate a password first.")

# --- GUI Setup ---
root = tk.Tk()
root.title("🔐 Advanced Password Generator")
root.geometry("450x400")
root.configure(bg="#eaf6f6")

# Heading
tk.Label(root, text="🔐 Password Generator", font=("Helvetica", 18, "bold"), bg="#eaf6f6", fg="#333").pack(pady=10)

# Frame for inputs
input_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief=tk.RIDGE, bd=2)
input_frame.pack(pady=10)

# Password length
tk.Label(input_frame, text="🔢 Password Length:", bg="#ffffff", font=("Arial", 12)).grid(row=0, column=0, sticky='w')
length_entry = tk.Entry(input_frame, width=10, font=("Arial", 12), justify='center')
length_entry.insert(0, "12")
length_entry.grid(row=0, column=1, padx=10, pady=10)

# Checkboxes for character types
letters_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(input_frame, text="📄 Letters (A-Z, a-z)", variable=letters_var, bg="#ffffff", font=("Arial", 11)).grid(row=1, column=0, columnspan=2, sticky='w')
tk.Checkbutton(input_frame, text="🔢 Digits (0-9)", variable=digits_var, bg="#ffffff", font=("Arial", 11)).grid(row=2, column=0, columnspan=2, sticky='w')
tk.Checkbutton(input_frame, text="✨ Symbols (!@#$...)", variable=symbols_var, bg="#ffffff", font=("Arial", 11)).grid(row=3, column=0, columnspan=2, sticky='w')

# Generate button
tk.Button(root, text="🚀 Generate Password", command=generate_password, font=("Arial", 12, "bold"), bg="#007bff", fg="white", padx=10, pady=5).pack(pady=15)
tk.Button(root, text="📋 Copy to Clipboard", command=copy_to_clipboard, ).pack()

# Output field
result_var = tk.StringVar()
tk.Entry(root, textvariable=result_var, font=("Consolas", 13), width=35, justify='center', bd=2, relief=tk.SUNKEN).pack(pady=5)

# Footer note
tk.Label(root, text="Tip: Select character types & click generate.", font=("Arial", 9), bg="#eaf6f6", fg="#555").pack(pady=5)

root.mainloop()
