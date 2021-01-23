import sys

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QGuiApplication

from PyQt5 import uic
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from text_edit_logger import QTextEditLogger
from services.bikesanity_service import BikeSanityService


class Ui(QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()

        ui = appctxt.get_resource('window.ui')
        uic.loadUi(ui, self)

        # Dependencies
        self.bikesanity_service = BikeSanityService()

        # Set visibility
        self.all_success_visible(False)

        # Event handlers
        self.downloadButton.clicked.connect(self.download_journal)
        self.processButton.clicked.connect(self.process_journal)
        self.publishButton.clicked.connect(self.publish_journal)

        self.downloadFromPage.stateChanged.connect(self.set_from_page_enabled)

        # Create logging widget
        logTextBox = QTextEditLogger(self)
        logTextBox.widget.setGeometry(10, 675, 521, 105)
        self.layout().addWidget(logTextBox.widget)


    def progress_callback(self, progress=None):
        if progress is not None:
            self.progressBar.setValue(progress)
        # Important for allowing the GUI loop to redraw and process all events
        QGuiApplication.processEvents()


    def set_from_page_enabled(self):
        self.downloadPageSpin.setEnabled(self.downloadFromPage.isChecked())

    def download_success_visible(self, visible):
        self.downloadSuccessLabel.setVisible(visible)
        self.downloadSuccessLink.setVisible(visible)

    def processed_success_visible(self, visible):
        self.processSuccessLabel.setVisible(visible)
        self.processSuccessLink.setVisible(visible)

    def published_success_visible(self, visible):
        self.publishedSuccessLabel.setVisible(visible)
        self.publishedSuccessLink.setVisible(visible)

    def all_success_visible(self, visible):
        self.download_success_visible(visible)
        self.processed_success_visible(visible)
        self.published_success_visible(visible)

    def disable_all_buttons(self):
        self.downloadButton.setEnabled(False)
        self.processButton.setEnabled(False)
        self.publishButton.setEnabled(False)

    def enable_all_buttons(self):
        self.downloadButton.setEnabled(True)
        self.processButton.setEnabled(True)
        self.publishButton.setEnabled(True)


    def download_journal(self):
        self.disable_all_buttons()

        journal_url = self.journalDownloadUrl.text()
        from_page = self.downloadPageSpin.value() if self.downloadFromPage.isChecked() else 0

        successful_download_location, journal_id = self.bikesanity_service.download_journal(
            journal_url, from_page=from_page, progress_callback=self.progress_callback
        )

        if successful_download_location:
            self.downloadSuccessLink.setText('<a href="{0}">{0}</a>'.format(successful_download_location))
            self.download_success_visible(True)
            self.processJournalId.setText(journal_id)
        else:
            self.download_success_visible(False)

        self.enable_all_buttons()


    def process_journal(self):
        self.disable_all_buttons()

        journal_id = self.processJournalId.text()
        exported = self.exportedJournalCheck.isChecked()

        successful_processed_location = self.bikesanity_service.process_journal(journal_id, exported=exported, progress_callback=self.progress_callback)
        if successful_processed_location:
            self.processSuccessLink.setText('<a href="{0}">{0}</a>'.format(successful_processed_location))
            self.processed_success_visible(True)
            self.publishJournalId.setText(journal_id)
        else:
            self.processed_success_visible(False)

        self.enable_all_buttons()


    def publish_journal(self):
        self.disable_all_buttons()

        journal_id = self.publishJournalId.text()
        successful_published_location = self.bikesanity_service.publish_journal(journal_id, progress_callback=self.progress_callback)
        if successful_published_location:
            self.publishedSuccessLink.setText('<a href="{0}">{0}</a>'.format(successful_published_location))
            self.published_success_visible(True)
        else:
            self.processed_success_visible(False)

        self.enable_all_buttons()



if __name__ == '__main__':
    appctxt = ApplicationContext()

    window = Ui()
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
