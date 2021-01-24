from PyQt5 import QtWidgets
import logging


class QTextEditLogger(logging.Handler):
    def __init__(self, textWidget):
        super().__init__()
        self.widget = textWidget
        self.widget.setReadOnly(True)
        self.init_logging()


    def init_logging(self):
        # You can format what is printed to text box
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self)
        # You can control the logging level
        logging.getLogger().setLevel(logging.INFO)


    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
