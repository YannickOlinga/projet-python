import tkinter as tk
from tkinter import messagebox

def register():
    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()
    address = entry_address.get()
    phone_number = entry_phone_number.get()

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
    else:
        messagebox.showinfo("Success", "Registration Successful")

app = tk.Tk()
app.title("Sign Up")
app.geometry("400x400")

label_username = tk.Label(app, text="Username")
label_username.pack(pady=5)
entry_username = tk.Entry(app)
entry_username.pack(pady=5)

label_password = tk.Label(app, text="Password")
label_password.pack(pady=5)
entry_password = tk.Entry(app, show="*")
entry_password.pack(pady=5)

label_confirm_password = tk.Label(app, text="Confirm Password")
label_confirm_password.pack(pady=5)
entry_confirm_password = tk.Entry(app, show="*")
entry_confirm_password.pack(pady=5)

label_address = tk.Label(app, text="Address")
label_address.pack(pady=5)
entry_address = tk.Entry(app)
entry_address.pack(pady=5)

label_phone_number = tk.Label(app, text="Phone Number")
label_phone_number.pack(pady=5)
entry_phone_number = tk.Entry(app)
entry_phone_number.pack(pady=5)

button_register = tk.Button(app, text="Register", command=register)
button_register.pack(pady=20)

app.mainloop()