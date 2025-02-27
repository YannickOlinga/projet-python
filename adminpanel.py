import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QVBoxLayout,
                             QHBoxLayout, QLabel, QTableView, QHeaderView,
                             QComboBox, QPushButton, QSpacerItem, QSizePolicy,
                             QFrame, QCheckBox, QAbstractItemView, QMessageBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5 import QtCore
from stock import StockUI  # Import your StockUI class
from fournisseur import FournisseurUI  # Import your FournisseurUI class
from facturation import FacturationUI  # Import your FacturationUI class

class PatientTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        self._headers = ["ID", "Name", "Age", "Telephone", "Email", "Address", "Carte"]

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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contacts")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #282c34; color: white;")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout()

        # Left Sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.create_profile_section())
        sidebar_layout.addWidget(self.create_navigation_button("Dashboard", self.go_to_dashboard))
        sidebar_layout.addWidget(self.create_navigation_button("Contacts Information", self.go_to_contacts))
        sidebar_layout.addWidget(self.create_navigation_button("Profile Form", self.go_to_profile_form))
        sidebar_layout.addWidget(self.create_navigation_button("Stock", self.go_to_stock))
        sidebar_layout.addWidget(self.create_navigation_button("Fournisseur", self.go_to_fournisseur))
        sidebar_layout.addWidget(self.create_navigation_button("Facturation", self.go_to_facturation))
        main_layout.addLayout(sidebar_layout)

        # Main Content Area
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.create_contacts_header())
        content_layout.addWidget(self.create_patient_table())
        content_layout.addWidget(self.create_pagination())
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def create_profile_section(self):
        profile_widget = QWidget()
        profile_layout = QVBoxLayout()

        # Profile Image
        pixmap = QPixmap("path/to/your/profile_image.jpg")  # Replace with your image path
        profile_image = QLabel()
        profile_image.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        profile_image.setAlignment(Qt.AlignCenter)
        profile_layout.addWidget(profile_image)

        # Name Label
        name_label = QLabel("Yannick OLINGA")
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFont(QFont("Arial", 14, QFont.Bold))
        profile_layout.addWidget(name_label)

        profile_widget.setLayout(profile_layout)
        return profile_widget

    def create_navigation_button(self, text, callback):
        button = QPushButton(text)
        button.setStyleSheet("text-align: left; padding: 10px; border: none; background-color: #383c44; color: white;")
        button.clicked.connect(callback)  # Connect the button click to the callback
        return button

    def create_contacts_header(self):
        header_widget = QWidget()
        header_layout = QVBoxLayout()

        contacts_label = QLabel("CONTACTS")
        contacts_label.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(contacts_label)

        patient_list_label = QLabel("Liste de patient enregistrer")
        header_layout.addWidget(patient_list_label)

        header_widget.setLayout(header_layout)
        return header_widget

    def create_patient_table(self):
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Sample data (replace with your actual data)
        data = [
            ["85ed5...", "admin", "N/A", "N/A", "yannickolinga213@...", "N/A", "N/A"],
            ["d5b7e...", "welldonw", "N/A", "697807256", "yannickolinga213@...", "N/A", "00000000"],
            ["2c667...", "ChristLove", "N/A", "697807256", "yannickolinga213@...", "N/A", "00000001"]
        ]
        model = PatientTableModel(data)
        self.table_view.setModel(model)
        return self.table_view

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

    def go_to_dashboard(self):
        QMessageBox.information(self, "Navigation", "Going to Dashboard...")

    def go_to_contacts(self):
        QMessageBox.information(self, "Navigation", "You are already on Contacts.")

    def go_to_profile_form(self):
        QMessageBox.information(self, "Navigation", "Going to Profile Form...")

    def go_to_stock(self):
        self.stock_ui = StockUI()
        self.stock_ui.show()
        self.close()  # Close current window

    def go_to_fournisseur(self):
        self.fournisseur_ui = FournisseurUI()
        self.fournisseur_ui.show()
        self.close()  # Close current window

    def go_to_facturation(self):
        self.facturation_ui = FacturationUI()
        self.facturation_ui.show()
        self.close()  # Close current window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactsUI()
    window.show()
    sys.exit(app.exec_())