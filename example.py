import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QPlainTextEdit


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.cnt = 0

    def initUI(self):
        x, y = 300, 300
        width, height = 800, 600
        self.setGeometry(x, y, width, height)
        self.setWindowTitle("Example program")

        self.label1 = QLabel(self)
        self.label1.resize(100, 100)
        self.label1.move(round(width * 0.1), round(height * 0.1))
        self.label1.setAlignment(Qt.AlignHCenter)

        self.label2 = QLabel("Имя:", self)
        self.label2.resize(100, 50)
        self.label2.move(round(width * 0.5), round(height * 0.07))
        self.label2.setAlignment(Qt.AlignHCenter)

        self.coords1 = QLabel("Координаты курсора: None, None", self)
        self.coords1.resize(width, 100)
        self.coords1.move(round(width * 0.1), round(height * 0.7))

        self.coords2 = QLabel("Никакая кнопка не была нажата", self)
        self.coords2.resize(width, 100)
        self.coords2.move(round(width * 0.1), round(height * 0.8))

        self.textPlain = QPlainTextEdit("", self)
        self.textPlain.resize(100, 40)
        self.textPlain.move(round(width * 0.5), round(height * 0.12))

        self.btn1 = QPushButton("Кнопка 1", self)
        self.btn1.resize(100, 100)
        self.btn1.move(round(width * 0.1), round(height * 0.2))
        self.btn1.clicked.connect(self.hello1)

        self.btn2 = QPushButton("Кнопка 2", self)
        self.btn2.resize(100, 100)
        self.btn2.move(round(width * 0.3), round(height * 0.2))
        self.btn2.clicked.connect(self.hello2)

        self.btn3 = QPushButton("Кнопка 3", self)
        self.btn3.resize(100, 100)
        self.btn3.move(round(width * 0.5), round(height * 0.2))
        self.btn3.clicked.connect(self.hello3)

        self.btn4 = QPushButton("Кликни", self)
        self.btn4.resize(100, 100)
        self.btn4.move(round(width * 0.7), round(height * 0.2))
        self.btn4.clicked.connect(self.clicker)

    def hello1(self):
        self.label1.setText("Привет")

    def hello2(self):
        print("Привет")

    def hello3(self):
        print(f"Привет, {self.textPlain.toPlainText()}")

    def clicker(self):
        self.cnt += 1
        self.btn4.setText(str(self.cnt))

    def mouseMoveEvent(self, event):
        self.coords1.setText(f"Координаты: {event.x()}, {event.y()}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.coords2.setText(f"Была нажата левая кнопка мыши в точке: {event.x()}, {event.y()}")
        elif event.button() == Qt.RightButton:
            self.coords2.setText(f"Была нажата правая кнопка мыши в точке: {event.x()}, {event.y()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
