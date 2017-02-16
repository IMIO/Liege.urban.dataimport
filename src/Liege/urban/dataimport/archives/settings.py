# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.settings import AccessImporterFromImportSettings

from Liege.urban.dataimport.archives.importer import ArchivesImporter


class ArchivesImporterFromImportSettings(AccessImporterFromImportSettings):
    """ """

    def __init__(self, settings_form, importer_class=ArchivesImporter):
        """
        """
        super(ArchivesImporterFromImportSettings, self).__init__(settings_form, importer_class)

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        settings = super(ArchivesImporterFromImportSettings, self).get_importer_settings()

        db_settings = {
            'db_name': 'Archives2013.mdb',
            'table_name': 'Global',
            'key_column': 'Numéro',
        }

        settings.update(db_settings)

        return settings
