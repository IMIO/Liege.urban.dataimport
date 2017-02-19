# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.settings import AccessImporterFromImportSettings

from Liege.urban.dataimport.buildlicence.importer import BuildlicenceImporter


class BuildlicenceImporterFromImportSettings(AccessImporterFromImportSettings):
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
            'db_name': 'P_tables.mdb',
            'table_name': 'PermisUrba_2017-02-17',
            'key_column': 'NUMDOSSIERBKP',
        }

        settings.update(db_settings)

        return settings
