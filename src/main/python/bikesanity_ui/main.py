import sys

from PyQt5.QtWidgets import QMainWindow

from PyQt5 import uic
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from services.bikesanity_service import BikeSanityService


class Ui(QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()

        ui = appctxt.get_resource('window.ui')
        uic.loadUi(ui, self)

        # Dependencies
        self.bikesanity_service = BikeSanityService()

        # Event handlers
        self.downloadButton.clicked.connect(self.download_journal)
        self.processButton.clicked.connect(self.process_journal)
        self.publishButton.clicked.connect(self.publish_journal)

    def download_journal(self):
        journal_url = self.journalDownloadUrl.text()
        self.bikesanity_service.download_journal(journal_url)

    def process_journal(self):
        journal_id = self.processJournalId.text()
        self.bikesanity_service.process_journal(journal_id)

    def publish_journal(self):
        journal_id = self.publishJournalId.text()
        self.bikesanity_service.publish_journal(journal_id)




if __name__ == '__main__':
    appctxt = ApplicationContext()

    window = Ui()
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
