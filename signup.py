import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3

class SignUpForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.conn = self.create_connection()
        self.create_table()

    def initUI(self):
        self.setWindowTitle('Sign Up Form')

        layout = QVBoxLayout()
        self.setFixedSize(400, 300)

        self.nameLabel = QLabel('Name:')
        self.nameInput = QLineEdit()
        self.nameLabel.setStyleSheet("font-size: 16px;")
        self.nameInput.setFixedHeight(30)
        self.nameInput.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.nameInput)

        self.emailLabel = QLabel('Email:')
        self.emailLabel.setStyleSheet("font-size: 16px;")
        self.emailInput = QLineEdit()
        self.emailInput.setFixedHeight(30)
        self.emailInput.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.emailLabel)
        layout.addWidget(self.emailInput)

        self.passwordLabel = QLabel('Password:')
        self.passwordLabel.setStyleSheet("font-size: 16px;")
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setFixedHeight(30)
        self.passwordInput.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordInput)

        self.confirmPasswordLabel = QLabel('Confirm Password:')
        self.confirmPasswordLabel.setStyleSheet("font-size: 16px;")
        self.confirmPasswordInput = QLineEdit()
        self.confirmPasswordInput.setEchoMode(QLineEdit.Password)
        self.confirmPasswordInput.setFixedHeight(30)
        self.confirmPasswordInput.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.confirmPasswordLabel)
        layout.addWidget(self.confirmPasswordInput)

        self.signUpButton = QPushButton('Sign Up')
        self.signUpButton.setFixedHeight(40)
        self.signUpButton.setStyleSheet("font-size: 16px;")
        self.signUpButton.clicked.connect(self.signUp)
        layout.addWidget(self.signUpButton)

        self.setLayout(layout)

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect('pharmacie.db')
            print("Connection to SQLite DB successful")
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")
        return conn

    def create_table(self):
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_users_table)
            print("Table created successfully")
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

    def signUp(self):
        name = self.nameInput.text()
        email = self.emailInput.text()
        password = self.passwordInput.text()
        confirmPassword = self.confirmPasswordInput.text()

        if password != confirmPassword:
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
            return

        user = (name, email, password)
        try:
            self.insert_user(user)
            QMessageBox.information(self, 'Success', f'You have successfully signed up!\nName: {name}\nEmail: {email}')
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Error', 'Email already exists')

    def insert_user(self, user):
        sql = ''' INSERT INTO users(name, email, password)
                  VALUES(?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, user)
        self.conn.commit()
        return cur.lastrowid

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = SignUpForm()
    form.show()
    sys.exit(app.exec_())