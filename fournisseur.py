import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class FournisseurUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fournisseur")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the Fournisseur Page"))
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FournisseurUI()
    window.show()
    sys.exit(app.exec_())