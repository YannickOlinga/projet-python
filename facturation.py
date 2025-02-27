import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class FacturationUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Facturation")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the Facturation Page"))
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FacturationUI()
    window.show()
    sys.exit(app.exec_())