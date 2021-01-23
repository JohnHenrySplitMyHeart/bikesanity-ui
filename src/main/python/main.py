from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMainWindow

import requests
import sys

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/window.ui', self)

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         text = QLabel()
#         text.setWordWrap(True)
#         button = QPushButton('Next quote >')
#         button.clicked.connect(lambda: text.setText(_get_quote()))
#         layout = QVBoxLayout()
#         layout.addWidget(text)
#         layout.addWidget(button)
#         layout.setAlignment(button, Qt.AlignHCenter)
#         self.setLayout(layout)

def _get_quote():
    return requests.get('https://build-system.fman.io/quote').text

if __name__ == '__main__':
    appctxt = ApplicationContext()
    stylesheet = appctxt.get_resource('styles.qss')
    #appctxt.app.setStyleSheet(open(stylesheet).read())
    window = Ui()
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
