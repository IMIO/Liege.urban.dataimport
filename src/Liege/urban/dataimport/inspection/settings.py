# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.settings import CSVImporterFromImportSettings

from Liege.urban.dataimport.inspection.importer import InspectionImporter


class InspectionImporterFromImportSettings(CSVImporterFromImportSettings):
    """ """

    def __init__(self, settings_form, importer_class=InspectionImporter):
        """
        """
        super(InspectionImporterFromImportSettings, self).__init__(settings_form, importer_class)

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        settings = super(InspectionImporterFromImportSettings, self).get_importer_settings()

        db_settings = {
            'csv_filename': 'INSP_RAPPORT_data1',
            'key_column': 'N°',
        }

        settings.update(db_settings)

        return settings
