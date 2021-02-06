import sys

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QGuiApplication

from PyQt5 import uic
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from text_edit_logger import QTextEditLogger
from services.bikesanity_service import BikeSanityService


class Ui(QMainWindow):

    VALID_URLS = [
        "https://www.crazyguyonabike.com",
        "http://www.crazyguyonabike.com",
        "https://crazyguyonabike.com",
        "http://crazyguyonabike.com"
    ]

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
        self.logTextBox = QTextEditLogger(self.logEdit)


    def progress_callback(self, progress=None):
        if progress is not None:
            self.progressBar.setValue(progress)
        # Important for allowing the GUI loop to redraw and process all events
        QGuiApplication.processEvents()


    def set_from_page_enabled(self):
        self.downloadPageSpin.setEnabled(self.downloadFromPage.isChecked())

    def retain_hidden_size(self, widget):
        policy = widget.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        widget.setSizePolicy(policy)

    def download_success_visible(self, visible):
        self.retain_hidden_size(self.downloadSuccessLabel)
        self.retain_hidden_size(self.downloadSuccessLink)
        self.downloadSuccessLabel.setVisible(visible)
        self.downloadSuccessLink.setVisible(visible)

    def processed_success_visible(self, visible):
        self.retain_hidden_size(self.processSuccessLabel)
        self.retain_hidden_size(self.processSuccessLink)
        self.processSuccessLabel.setVisible(visible)
        self.processSuccessLink.setVisible(visible)

    def published_success_visible(self, visible):
        self.retain_hidden_size(self.publishedSuccessLabel)
        self.retain_hidden_size(self.publishedSuccessLink)
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

    def show_error_label(self, message, label, link):
        label.setText(message)
        label.setVisible(True)
        link.setVisible(False)
        self.enable_all_buttons()
        return


    def sanitize_file_link(self, location):
        sanitized = location.replace('\\', '/').replace(' ', '%20')
        return '<a href="{0}">{1}</a>'.format(sanitized, location)

    def download_journal(self):
        self.disable_all_buttons()

        journal_url = self.journalDownloadUrl.text()
        from_page = self.downloadPageSpin.value() if self.downloadFromPage.isChecked() else 0

        if journal_url.startswith('www') or journal_url.startswith('WWW'):
            journal_url = 'https://' + journal_url

        if not journal_url or not any([journal_url.startswith(valid_url) for valid_url in self.VALID_URLS]):
            self.show_error_label('Needs to be a URL to a CGOAB journal', self.downloadSuccessLabel, self.downloadSuccessLink)
            return

        successful_download_location, journal_id = self.bikesanity_service.download_journal(
            journal_url, from_page=from_page, progress_callback=self.progress_callback
        )

        if successful_download_location:
            self.downloadSuccessLabel.setText('Downloaded journal available at:')
            self.downloadSuccessLink.setText(self.sanitize_file_link(successful_download_location))
            self.download_success_visible(True)
            self.processJournalId.setText(journal_id)
        else:
            self.show_error_label('Download did not complete', self.downloadSuccessLabel, self.downloadSuccessLink)

        self.enable_all_buttons()

    def process_journal(self):
        self.disable_all_buttons()

        journal_id = self.processJournalId.text()
        exported = self.exportedJournalCheck.isChecked()

        if not journal_id:
            self.show_error_label('Please enter a journal ID, e.g. 12345', self.processSuccessLabel, self.processSuccessLink)
            return
        if not journal_id.isdigit():
            self.show_error_label('Journal IDs should be numeric, e.g. 12345', self.processSuccessLabel, self.processSuccessLink)
            return

        successful_processed_location = self.bikesanity_service.process_journal(journal_id, exported=exported, progress_callback=self.progress_callback)
        if successful_processed_location:
            self.processSuccessLabel.setText('Processed journal available at:')
            self.processSuccessLink.setText(self.sanitize_file_link(successful_processed_location))
            self.processed_success_visible(True)
            self.publishJournalId.setText(journal_id)
        else:
            self.show_error_label('Processing did not complete!', self.processSuccessLabel, self.processSuccessLink)

        self.enable_all_buttons()


    def publish_journal(self):
        self.disable_all_buttons()

        journal_id = self.publishJournalId.text()

        if not journal_id:
            self.show_error_label('Please enter a journal ID, e.g. 12345', self.publishedSuccessLabel, self.publishedSuccessLink)
            return
        if not journal_id.isdigit():
            self.show_error_label('Journal IDs should be numeric, e.g. 12345', self.publishedSuccessLabel, self.publishedSuccessLink)
            return

        html = self.htmlFormat.isChecked()
        pdf = self.pdfFormat.isChecked()
        json = self.jsonFormat.isChecked()

        successful_published_location = self.bikesanity_service.publish_journal(
            journal_id, progress_callback=self.progress_callback, html=html, pdf=pdf, json=json
        )

        if successful_published_location:
            self.publishedSuccessLabel.setText('Published journal available at:')
            self.publishedSuccessLink.setText(self.sanitize_file_link(successful_published_location))
            self.published_success_visible(True)
        else:
            self.show_error_label('Publication did not complete!', self.publishedSuccessLabel, self.publishedSuccessLink)

        self.enable_all_buttons()


if __name__ == '__main__':
    appctxt = ApplicationContext()

    window = Ui()
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
