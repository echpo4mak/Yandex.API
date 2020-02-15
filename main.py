import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.label.setText("OK")


app = QApplication(sys.argv)
ex = Map()
ex.show()
sys.exit(app.exec_())
