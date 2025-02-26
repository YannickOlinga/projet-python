import tkinter as tk
from tkinter import messagebox

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == "admin" and password == "password":
        messagebox.showinfo("Login", "Login Successful")
    else:
        messagebox.showerror("Login", "Invalid Username or Password")

# Create the main window
root = tk.Tk()
root.title("Login")
root.geometry("400x300")  # Set the window size

# Define a larger font
font_large = ("Helvetica", 14)

# Create and place the username label and entry
label_username = tk.Label(root, text="Username", font=font_large)
label_username.pack(pady=10)
entry_username = tk.Entry(root, font=font_large)
entry_username.pack(pady=10, ipadx=10, ipady=5)

# Create and place the password label and entry
label_password = tk.Label(root, text="Password", font=font_large)
label_password.pack(pady=10)
entry_password = tk.Entry(root, show="*", font=font_large)
entry_password.pack(pady=10, ipadx=10, ipady=5)

# Create and place the login button
button_login = tk.Button(root, text="Login", command=login, font=font_large)
button_login.pack(pady=20, ipadx=10, ipady=5)

# Run the application
root.mainloop()