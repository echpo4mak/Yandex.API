import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
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

        self.geocoder_params = {
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
            'geocode': None,
            'format': 'json'
        }

        self.find_button.clicked.connect(self.find_address)

        self.getImage()
        self.show_map()

    def find_address(self):
        self.geocoder_params['geocode'] = self.address_input.text()
        geocoder_response = requests.get('http://geocode-maps.yandex.ru/1.x/', params=self.geocoder_params)

        if not geocoder_response:
            print("Ошибка выполнения запроса:")
            print("Http статус: ", geocoder_response.status_code, " (", geocoder_response.reason, ")", sep='')
            sys.exit(1)

        json_response = geocoder_response.json()
        toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        self.params['ll'] = toponym["Point"]["pos"].replace(' ', ',')
        self.params['pt'] = self.params['ll'] + ',pm2rdm'

        self.getImage()
        self.show_map()

    def getImage(self):
        response = requests.get('http://static-maps.yandex.ru/1.x/', params=self.params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус: ", response.status_code, " (", response.reason, ")", sep='')
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as f:
            f.write(response.content)

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

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.move_map(0, 1)
        elif event.key() == Qt.Key_Down:
            self.move_map(0, -1)
        elif event.key() == Qt.Key_Left:
            self.move_map(-1, 0)
        elif event.key() == Qt.Key_Right:
            self.move_map(1, 0)

    def move_map(self, x, y):
        x_shift = float(self.params['spn'].split(',')[0]) * x
        y_shift = float(self.params['spn'].split(',')[1]) * y
        new_ll = self.params['ll'].split(',')
        new_ll[0] = float(new_ll[0]) + x_shift
        new_ll[1] = float(new_ll[1]) + y_shift
        self.params['ll'] = ','.join(map(str, new_ll))
        self.getImage()
        self.show_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pr = Map()
    pr.show()
    sys.exit(app.exec())
