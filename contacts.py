import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QTableView, QHeaderView,
                             QComboBox, QPushButton, QAbstractItemView, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QAbstractTableModel
from contact_infos import ContactInfoUI  # Importer ContactInfoUI

class PatientTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        self._headers = ["ID", "Name", "Email"]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None

class ContactsUI(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username  # Store the username
        self.setWindowTitle("Utilisateurs")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #282c34; color: white;")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout()  # Use a horizontal layout for the main layout

        # Sidebar
        sidebar_layout = QVBoxLayout()
        
        # Add username label to the sidebar
        username_label = QLabel(f"Connecté: {self.username}")
        username_label.setFont(QFont("Arial", 12))
        sidebar_layout.addWidget(username_label)

        # Create buttons and connect them
        sidebar_layout.addWidget(self.create_navigation_button("Compte", self.open_contact_info))
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
        content_layout.addWidget(self.create_contacts_header())
        content_layout.addWidget(self.create_patient_table())
        content_layout.addWidget(self.create_pagination())
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def create_navigation_button(self, text, callback=None):
        button = QPushButton(text)
        button.setStyleSheet("text-align: left; padding: 10px; border: none; background-color: #383c44; color: white;")
        if callback:
            button.clicked.connect(callback)  # Connect the button to the callback
        return button

    def create_contacts_header(self):
        header_widget = QWidget()
        header_layout = QVBoxLayout()
        contacts_label = QLabel("Utilisateurs")
        contacts_label.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(contacts_label)
        patient_list_label = QLabel("Liste des utilisateurs enregistrés")
        header_layout.addWidget(patient_list_label)
        header_widget.setLayout(header_layout)
        return header_widget

    def create_patient_table(self):
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Récupérer les données des utilisateurs
        data = self.get_users_from_db()
        model = PatientTableModel(data)
        self.table_view.setModel(model)
        return self.table_view

    def get_users_from_db(self):
        conn = None
        users = []
        try:
            conn = sqlite3.connect('pharmacie.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users")
            users = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
        finally:
            if conn:
                conn.close()
        return users

    def create_pagination(self):
        pagination_widget = QWidget()
        pagination_layout = QHBoxLayout()
        rows_label = QLabel("Rows per page:")
        pagination_layout.addWidget(rows_label)

        rows_combo = QComboBox()
        rows_combo.addItems(["10", "20", "50", "100"])
        pagination_layout.addWidget(rows_combo)

        page_label = QLabel("1-3 of 3")
        pagination_layout.addWidget(page_label)

        prev_button = QPushButton("<")
        pagination_layout.addWidget(prev_button)

        next_button = QPushButton(">")
        pagination_layout.addWidget(next_button)

        pagination_widget.setLayout(pagination_layout)
        return pagination_widget

    def open_contact_info(self):
        self.contact_info_ui = ContactInfoUI(self.username)  # Pass the username to ContactInfoUI
        self.contact_info_ui.show()  # Show the new window
        self.close()  # Close the current window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactsUI("Utilisateur Test")  # Replace with actual username
    window.show()
    sys.exit(app.exec_())