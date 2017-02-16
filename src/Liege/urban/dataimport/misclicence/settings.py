# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.settings import AccessImporterFromImportSettings

from Liege.urban.dataimport.misclicence.importer import MisclicenceImporter


class MisclicenceImporterFromImportSettings(AccessImporterFromImportSettings):
    """ """

    def __init__(self, settings_form, importer_class=MisclicenceImporter):
        """
        """
        super(MisclicenceImporterFromImportSettings, self).__init__(settings_form, importer_class)

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        settings = super(MisclicenceImporterFromImportSettings, self).get_importer_settings()

        db_settings = {
            'db_name': 'P_tables.mdb',
            'table_name': 'T Aff Diverses',
            'key_column': 'DOSSIER',
        }

        settings.update(db_settings)

        return settings
