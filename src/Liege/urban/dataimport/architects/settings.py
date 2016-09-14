# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.settings import AccessImporterFromImportSettings

from Liege.urban.dataimport.architects.importer import ArchitectsImporter


class ArchitectsImporterFromImportSettings(AccessImporterFromImportSettings):
    """ """

    def __init__(self, settings_form, importer_class=ArchitectsImporter):
        """
        """
        super(ArchitectsImporterFromImportSettings, self).__init__(settings_form, importer_class)

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        settings = super(ArchitectsImporterFromImportSettings, self).get_importer_settings()

        db_settings = {
            'db_name': 'P_tables.mdb',
            'table_name': 'T Architecte',
            'key_column': 'Numéro',
        }

        settings.update(db_settings)

        return settings
