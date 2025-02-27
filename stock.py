import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTableView, QHeaderView, QAbstractItemView,
                             QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QAbstractTableModel

class MedicamentTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        self._headers = ["ID", "Nom", "Quantité", "Prix"]

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

class StockUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Médicaments")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #282c34; color: white;")
        self.setup_ui()
        self.load_medicaments()  # Load initial data

    def setup_ui(self):
        main_layout = QHBoxLayout()  # Use a horizontal layout for the main layout

        # Sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.create_navigation_button("Compte"))
        sidebar_layout.addWidget(self.create_navigation_button("Profile Form"))
        sidebar_layout.addWidget(self.create_navigation_button("Stock"))  # Just for display, no action
        sidebar_layout.addWidget(self.create_navigation_button("Fournisseur"))
        sidebar_layout.addWidget(self.create_navigation_button("Facturation"))

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setStyleSheet("background-color: #383c44;")  # Style the sidebar
        main_layout.addWidget(sidebar_widget)

        # Main Content Area
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.create_medicament_form())
        content_layout.addWidget(self.create_medicament_table())
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def create_navigation_button(self, text, callback=None):
        button = QPushButton(text)
        button.setStyleSheet("text-align: left; padding: 10px; border: none; background-color: #383c44; color: white;")
        if callback:
            button.clicked.connect(callback)
        return button

    def create_medicament_form(self):
        form_widget = QWidget()
        form_layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom du médicament")

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantité")

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Prix")

        # Buttons
        add_button = QPushButton("Ajouter")
        add_button.clicked.connect(self.add_medicament)

        update_button = QPushButton("Modifier")
        update_button.clicked.connect(self.update_medicament)

        delete_button = QPushButton("Supprimer")
        delete_button.clicked.connect(self.delete_medicament)

        # Add fields to the layout
        form_layout.addWidget(QLabel("Ajouter / Modifier Médicament"))
        form_layout.addWidget(QLabel("Nom:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Quantité:"))
        form_layout.addWidget(self.quantity_input)
        form_layout.addWidget(QLabel("Prix:"))
        form_layout.addWidget(self.price_input)
        form_layout.addWidget(add_button)
        form_layout.addWidget(update_button)
        form_layout.addWidget(delete_button)

        form_widget.setLayout(form_layout)
        return form_widget

    def create_medicament_table(self):
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.clicked.connect(self.load_selected_medicament)  # Load selected medicament info

        return self.table_view

    def load_medicaments(self):
        """Load medicaments from the database into the table."""
        conn = None
        try:
            conn = sqlite3.connect('pharmacie.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, quantity, price FROM medicaments")
            medicaments = cursor.fetchall()
            model = MedicamentTableModel(medicaments)
            self.table_view.setModel(model)
        except sqlite3.Error as e:
            QMessageBox.warning(self, 'Erreur', f'Erreur lors du chargement des médicaments: {e}')
        finally:
            if conn:
                conn.close()

    def add_medicament(self):
        name = self.name_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()

        conn = None
        try:
            conn = sqlite3.connect('pharmacie.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO medicaments (name, quantity, price) VALUES (?, ?, ?)",
                           (name, quantity, price))
            conn.commit()
            QMessageBox.information(self, 'Succès', 'Médicament ajouté avec succès.')
            self.load_medicaments()  # Reload the medicaments
        except sqlite3.Error as e:
            QMessageBox.warning(self, 'Erreur', f'Erreur lors de l\'ajout: {e}')
        finally:
            if conn:
                conn.close()

    def update_medicament(self):
        selected_index = self.table_view.selectionModel().currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner un médicament à modifier.')
            return

        medicament_id = self.table_view.model().data(selected_index.sibling(selected_index.row(), 0))
        name = self.name_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()

        conn = None
        try:
            conn = sqlite3.connect('pharmacie.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE medicaments SET name=?, quantity=?, price=? WHERE id=?",
                           (name, quantity, price, medicament_id))
            conn.commit()
            QMessageBox.information(self, 'Succès', 'Médicament modifié avec succès.')
            self.load_medicaments()  # Reload the medicaments
        except sqlite3.Error as e:
            QMessageBox.warning(self, 'Erreur', f'Erreur lors de la modification: {e}')
        finally:
            if conn:
                conn.close()

    def delete_medicament(self):
        selected_index = self.table_view.selectionModel().currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner un médicament à supprimer.')
            return

        medicament_id = self.table_view.model().data(selected_index.sibling(selected_index.row(), 0))

        conn = None
        try:
            conn = sqlite3.connect('pharmacie.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM medicaments WHERE id=?", (medicament_id,))
            conn.commit()
            QMessageBox.information(self, 'Succès', 'Médicament supprimé avec succès.')
            self.load_medicaments()  # Reload the medicaments
        except sqlite3.Error as e:
            QMessageBox.warning(self, 'Erreur', f'Erreur lors de la suppression: {e}')
        finally:
            if conn:
                conn.close()

   def load_selected_medicament(self):
    selected_index = self.table_view.selectionModel().currentIndex()
    if not selected_index.isValid():
        return

    medicament_id = self.table_view.model().data(selected_index.sibling(selected_index.row(), 0), Qt.DisplayRole)
    conn = None
    try:
        conn = sqlite3.connect('pharmacie.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity, price FROM medicaments WHERE id=?", (medicament_id,))
        medicament = cursor.fetchone()
        if medicament:
            self.name_input.setText(medicament[0])
            self.quantity_input.setText(str(medicament[1]))
            self.price_input.setText(str(medicament[2]))
    except sqlite3.Error as e:
        QMessageBox.warning(self, 'Erreur', f'Erreur lors du chargement des informations: {e}')
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockUI()
    window.show()
    sys.exit(app.exec_())