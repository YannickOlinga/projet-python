import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QMessageBox)
from signup import SignUpForm  # Import the SignUpForm
from contacts import ContactsUI  # Import ContactsUI

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.create_table()  # Create the table when the form is initialized

    def initUI(self):
        self.setWindowTitle('Login Form')
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()

        self.label_name = QLabel('Name:')
        self.input_name = QLineEdit()
        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)

        self.label_password = QLabel('Password:')
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        self.button_login = QPushButton('Login')
        self.button_login.clicked.connect(self.check_credentials)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect('pharmacie.db')
        except sqlite3.Error as e:
            print(e)
        return conn

    def create_table(self):
        conn = self.create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL);''')
                conn.commit()
            except sqlite3.Error as e:
                print(e)
            finally:
                conn.close()

    def check_user(self, name, password):
        conn = self.create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute('SELECT * FROM users WHERE name=? AND password=?', (name, password))
                user = c.fetchone()
                return user is not None
            except sqlite3.Error as e:
                print(e)
            finally:
                conn.close()
        return False

    def check_credentials(self):
        name = self.input_name.text()
        password = self.input_password.text()

        if self.check_user(name, password):
            QMessageBox.information(self, 'Success', 'Login Successful')
            self.open_contacts_ui()  # Open ContactsUI
        else:
            reply = QMessageBox.question(self, 'Account Not Found', 
                                          'User not found. Would you like to create an account?', 
                                          QMessageBox.Yes | QMessageBox.No, 
                                          QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.open_signup()

    def open_signup(self):
        self.signup_form = SignUpForm()
        self.signup_form.show()

    def open_contacts_ui(self):
        username = self.input_name.text()  # Récupérer le nom de l'utilisateur
        self.contacts_ui = ContactsUI(username)  # Passer le nom d'utilisateur à ContactsUI
        self.contacts_ui.show()           # Show ContactsUI
        self.close()                      # Close the login form

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()
    sys.exit(app.exec_())