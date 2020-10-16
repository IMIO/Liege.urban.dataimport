# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.settings import CSVImporterFromImportSettings

from Liege.urban.dataimport.inspection_misclicence.importer import InspectionMisclicenceImporter


class InspectionMisclicenceImporterFromImportSettings(CSVImporterFromImportSettings):
    """ """

    def __init__(self, settings_form, importer_class=InspectionMisclicenceImporter):
        """
        """
        super(InspectionMisclicenceImporterFromImportSettings, self).__init__(settings_form, importer_class)

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        settings = super(InspectionMisclicenceImporterFromImportSettings, self).get_importer_settings()

        db_settings = {
            'csv_filename': 'T Aff Diverses',
            'key_column': 'DOSSIER',
        }

        settings.update(db_settings)

        return settings
