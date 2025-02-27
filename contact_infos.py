import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ContactInfoUI(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username  # Store the username
        self.setWindowTitle("Modifier les Informations de Compte")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #282c34; color: white;")
        self.setup_ui()
        self.load_user_info()  # Load the user's current information

    def setup_ui(self):
        main_layout = QHBoxLayout()  # Use a horizontal layout for the main layout

        # Sidebar
        sidebar_layout = QVBoxLayout()
        
        # Add username label to the sidebar
        username_label = QLabel(f"Connecté: {self.username}")
        username_label.setFont(QFont("Arial", 12))
        sidebar_layout.addWidget(username_label)

        sidebar_layout.addWidget(self.create_navigation_button("Compte"))
        sidebar_layout.addWidget(self.create_navigation_button("Profile Form"))
        sidebar_layout.addWidget(self.create_navigation_button("Stock"))
        sidebar_layout.addWidget(self.create_navigation_button("Fournisseur"))
        sidebar_layout.addWidget(self.create_navigation_button("Facturation"))
        
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setStyleSheet("background-color: #383c44;")  # Style the sidebar
        main_layout.addWidget(sidebar_widget)

        # Main Content Area
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.create_contact_info_form())
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def create_navigation_button(self, text):
        button = QPushButton(text)
        button.setStyleSheet("text-align: left; padding: 10px; border: none; background-color: #383c44; color: white;")
        return button

    def create_contact_info_form(self):
        form_widget = QWidget()
        form_layout = QVBoxLayout()

        # Create form fields
        name_label = QLabel("Nom:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Entrez votre nom")
        
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Entrez votre email")

        password_label = QLabel("Mot de passe:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Entrez votre mot de passe")

        # Save button
        save_button = QPushButton("Sauvegarder")
        save_button.clicked.connect(self.save_changes)

        # Add fields to the layout
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(save_button)

        form_widget.setLayout(form_layout)
        return form_widget

    def load_user_info(self):
        """Load user information from the database into the input fields."""
        conn = None
        try:
            conn = sqlite3.connect('pharmacie.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name, email FROM users WHERE name=?", (self.username,))
            user_info = cursor.fetchone()
            if user_info:
                self.name_input.setText(user_info[0])
                self.email_input.setText(user_info[1])
        except sqlite3.Error as e:
            QMessageBox.warning(self, 'Erreur', f'Erreur lors du chargement des informations: {e}')
        finally:
            if conn:
                conn.close()

    def save_changes(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        # Update user info in the database
        conn = None
        try:
            conn = sqlite3.connect('pharmacie.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET name=?, email=?, password=? WHERE name=?',
                           (name, email, password, self.username))
            conn.commit()
            QMessageBox.information(self, 'Succès', 'Informations mises à jour avec succès.')
            self.username = name  # Update the stored username
            self.load_user_info()  # Reload the user info to reflect changes
        except sqlite3.Error as e:
            QMessageBox.warning(self, 'Erreur', f'Erreur lors de la mise à jour: {e}')
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactInfoUI("Utilisateur Test")  # Replace with actual username
    window.show()
    sys.exit(app.exec_())