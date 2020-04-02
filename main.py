import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.params = {
            'll': '37.530887,55.703118',
            'spn': '0.002,0.002',
            'l': 'map',
            'size': '650,450'
        }
        self.map_btn.toggled.connect(self.layerChange)
        self.map_btn.setChecked(True)
        self.sat_btn.toggled.connect(self.layerChange)
        self.hyb_btn.toggled.connect(self.layerChange)
        self.getImage()
        self.show_map()

    def getImage(self):
        response = requests.get('http://static-maps.yandex.ru/1.x/', params=self.params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def show_map(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.coords.setText(f'Координаты: {self.params["ll"]}')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_P:
            self.params['spn'] = ','.join(list(map(lambda x: str(float(x) + 0.001)
            if float(x) < 50 else x, self.params['spn'].split(','))))
        elif event.key() == Qt.Key_M:
            self.params['spn'] = ','.join(list(map(lambda x: str(float(x) - 0.001)
            if float(x) > 0 else x, self.params['spn'].split(','))))
        self.getImage()
        self.show_map()

    def layerChange(self):
        if self.sender() == self.map_btn:
            self.params['l'] = 'map'
        elif self.sender() == self.sat_btn:
            self.params['l'] = 'sat'
        elif self.sender() == self.hyb_btn:
            self.params['l'] = 'sat,skl'
        self.getImage()
        self.show_map()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pr = Map()
    pr.show()
    sys.exit(app.exec())
