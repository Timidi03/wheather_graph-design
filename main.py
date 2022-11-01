import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtGui
import requests
from bs4 import BeautifulSoup


class weather(QMainWindow):
    def __init__(self):
        super(weather, self).__init__()
        loadUi('Weather.ui', self)
        self.pushButton.clicked.connect(self.get_weather)
        self.pushButton.clicked.connect(self._on_add_1)
        self.number = -1

    def get_weather(self):
        global city
        city = self.plainTextEdit.toPlainText().lower()
        try:
            url = f'https://sinoptik.ua/погода-{city}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            global data_day
            data_day = soup.find('p', class_='day-link')
            global data_description
            data_description = soup.find("div", class_ = 'description')
            global data_min
            data_min = soup.find('div', class_='min')
            global data_max
            data_max = soup.find('div', class_='max')
            global data_date
            data_date = soup.find('p', class_='date')
            global data_month
            data_month = soup.find('p', class_='month')
            self.textEdit_1.setText(data_day.text)
            self.textEdit_2.setText(f'{data_date.text} {data_month.text}')
            self.textEdit_3.setText(data_description.text)
            self.textEdit_4.setText(data_min.text)
            self.textEdit_5.setText(data_max.text)

        except EOFError:
            self.textEdit.setText('Такого города не существует либо вы неправильно его ввели!')

    def _on_add_1(self):
        self.number += 1
        self.tableWidget.setItem(self.number, 0, QTableWidgetItem(str(self.plainTextEdit.toPlainText())))
        self.tableWidget.setItem(self.number, 1, QTableWidgetItem(
            str(f'Сегодня {data_day.text} {data_date.text} {data_month.text} в '
                f'{city} температура воздуха {data_min.text}, а {data_max.text}')))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = weather()
    widget.show()
    sys.exit(app.exec_())
