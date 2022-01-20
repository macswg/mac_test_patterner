from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("Test Pattern Maker")

    label = QtWidgets.QLabel(win)
    label.setText("Label Here")
    label.move(50, 50)

    win.show()
    sys.exit(app.exec())

window()