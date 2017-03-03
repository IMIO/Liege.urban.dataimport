# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.settings import CSVImporterFromImportSettings

from Liege.urban.dataimport.buildlicence.importer import BuildlicenceImporter


class BuildlicenceImporterFromImportSettings(CSVImporterFromImportSettings):
    """ """

    def __init__(self, settings_form, importer_class=BuildlicenceImporter):
        """
        """
        super(BuildlicenceImporterFromImportSettings, self).__init__(settings_form, importer_class)

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        settings = super(BuildlicenceImporterFromImportSettings, self).get_importer_settings()

        db_settings = {
            'csv_filename': 'PermisUrba',
            'key_column': 'NUMDOSSIERBKP',
        }

        settings.update(db_settings)

        return settings
