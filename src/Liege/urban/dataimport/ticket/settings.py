# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.settings import CSVImporterFromImportSettings

from Liege.urban.dataimport.ticket.importer import TicketImporter


class TicketImporterFromImportSettings(CSVImporterFromImportSettings):
    """ """

    def __init__(self, settings_form, importer_class=TicketImporter):
        """
        """
        super(TicketImporterFromImportSettings, self).__init__(settings_form, importer_class)

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        settings = super(TicketImporterFromImportSettings, self).get_importer_settings()

        db_settings = {
            'csv_filename': 'PVerbaux_data',
            'key_column': 'NUMERO',
        }

        settings.update(db_settings)

        return settings
