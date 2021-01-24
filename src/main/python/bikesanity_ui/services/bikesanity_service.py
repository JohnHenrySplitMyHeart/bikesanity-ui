import os
from pathlib import Path
import logging

from bikesanity.processing.download_journal import DownloadJournal
from bikesanity.processing.load_disk_journal import LoadDiskJournal
from bikesanity.processing.publish_journal import PublishJournal, PublicationFormats


BASE_DIRECTORY = 'CycleSanityJournals'


class BikeSanityService:

    def __init__(self):
        self.base_path = os.path.join(Path.home(), BASE_DIRECTORY)

    def download_journal(self, journal_link, location=None, no_local_readability_postprocessing=False, from_page=0, progress_callback=None):
        logging.info('Starting download task...')

        download_path = location if location else self.base_path

        # Download the journal
        try:
            journal_downloader = DownloadJournal(download_path, progress_callback=progress_callback)
            journal = journal_downloader.download_journal_url(journal_link, from_page)

            download_location = journal_downloader.get_download_location(journal)

            if not journal or not download_location:
                raise RuntimeError('Unexpected error when downloading journal: {0}'.format(journal_link))

            logging.info('Completed download task! Journal {0} downloaded to {1}'.format(journal.journal_id, download_location))
            return download_location, journal.journal_id
        except Exception:
            logging.exception('Critical error on downloading journal')

    def process_journal(self, journal_id, exported, input_location=None, output_location=None, progress_callback=None):
        logging.info('Processing journal id {0}'.format(journal_id))

        input_path = input_location if input_location else self.base_path
        output_path = output_location if output_location else self.base_path

        try:
            journal_processor = LoadDiskJournal(input_path, output_path, journal_id, exported=False, progress_callback=progress_callback)
            journal = journal_processor.load_journal_from_disk()

            process_location = journal_processor.get_process_location()
            logging.info('Completed processing task! Processed journal available in {0}'.format(process_location))
            return process_location

        except Exception:
            logging.exception('Critical error on processing journal')
            return None

    def publish_journal(self, journal_id, input_location=None, output_location=None, html=True, pdf=False, epub=False, progress_callback=None):
        logging.info('Outputting journal id {0} to formats: {1}'.format(journal_id, 'html'))

        input_path = input_location if input_location else self.base_path
        output_path = output_location if output_location else self.base_path

        try:
            journal_publisher = PublishJournal(input_path, output_path, journal_id)
            journal_publisher.publish_journal_id(PublicationFormats.TEMPLATED_HTML, progress_callback=progress_callback)

            publication_location = journal_publisher.get_publication_location()
            logging.info('Completed publishing to HTML! Published journal available in {0}'.format(publication_location))
            return publication_location

        except Exception:
            logging.exception('Critical error on publishing journal')
