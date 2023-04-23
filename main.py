import sys

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel

from solve import getQuad, getQuad_long


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.start_x, self.start_y = 300, 300  # координата левого верхнего угла на экране монитора
        self.width, self.height = 1200, 900  # размер окна
        self.scale = 1  # масштаб (скоро)
        self.c_x, self.c_y = self.width // 2, self.height // 2  # центр сетки координат
        self.my_dots = list()  # список всех точек
        self.initUI()

    def initUI(self):  # инициализация кнопочек
        self.setGeometry(self.start_x, self.start_y, self.width, self.height)
        self.setWindowTitle("Search max area")

        self.clear_btn = QPushButton("Очистить", self)
        self.clear_btn.resize(180, 100)
        self.clear_btn.move(round(self.width * 0.01), round(self.height * 0.01))
        self.clear_btn.clicked.connect(self.clear)

    def mousePressEvent(self, event):  # считывание точек с мышки
        x, y = event.x(), event.y()  # получаем координаты клика
        self.my_dots.append(((x - self.c_x + (self.scale - 1)) // self.scale, (self.c_y - y) // self.scale))
        # добавляем точку в массив
        self.update()  # обновляем окно

    def clear(self):  # очистка окна
        self.my_dots.clear()  # очищаем массив
        self.update()  # обновляем окно

    def paintEvent(self, event):
        painter = QPainter()  # создаём "кисть"
        painter.begin(self)  # "опускаем кисть на холст"
        self.drawGrid(painter)  # рисуем "сетку координат"
        self.drawDots(painter)  # рисуем все точки
        self.drawQaud(painter)  # рисуем четырёхугольник (ответ)
        painter.end()  # "подымаем кисть"

    def drawDots(self, painter):  # рисует точки
        painter.setPen(QPen(Qt.gray, 5))  # выбираем цвет
        for x, y in self.my_dots:  # перебираем координаты всех точек
            # рисуем точку в виде маленького кружочка
            painter.drawEllipse(self.c_x + x * self.scale, self.c_y - y * self.scale, 2, 2)

    def drawQaud(self, painter):
        painter.setPen(QPen(Qt.green, 3))  # выбираем цвет
        dots = list()  # инициализируем массив
        for x, y in getQuad(self.my_dots.copy()):  # перебираем все точки из массива, который получаем в solve.getQuad
            # преобразуем tuple -> QPoint с необходимыми преобразованиями и добавляем в массив
            dots.append(QPoint(self.c_x + x * self.scale, self.c_y - y * self.scale))
        painter.drawPolygon(dots)  # рисуем четырёхугольник

        painter.setPen(QPen(Qt.red, 2))  # выбираем цвет
        dots = list()  # инициализируем массив
        for x, y in getQuad_long(
                self.my_dots.copy()):  # перебираем все точки из массива, который получаем в solve.getQuad
            # преобразуем tuple -> QPoint с необходимыми преобразованиями и добавляем в массив
            dots.append(QPoint(self.c_x + x * self.scale, self.c_y - y * self.scale))
        painter.drawPolygon(dots)  # рисуем четырёхугольник

    def drawGrid(self, painter):
        # рисует сетку координат
        painter.setPen(QPen(Qt.black, 2))  # выбираем цвет
        painter.drawLine(0, self.c_y, self.width, self.c_y)  # рисуем горизонтальную линию
        painter.drawLine(self.c_x, 0, self.c_x, self.height)  # рисуем вертикальную линию
        # определяем точки для многоугольника "стрелочка"
        xArrow = [QPoint(self.width - 10, self.c_y - 5), QPoint(self.width - 1, self.c_y),
                  QPoint(self.width - 10, self.c_y + 5)]
        yArrow = [QPoint(self.c_x - 5, 10), QPoint(self.c_x, 1),
                  QPoint(self.c_x + 5, 10)]
        # рисуем стрелочки
        painter.drawPolygon(xArrow)
        painter.drawPolygon(yArrow)


# фишка питона, чтобы запускался только этот файл: те, которые мы импортируем, без команды этого файла ничего не делали
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())
