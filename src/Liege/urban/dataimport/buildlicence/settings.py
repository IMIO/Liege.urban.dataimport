# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.settings import AccessImporterFromImportSettings


class BuildlicenceImporterFromImportSettings(AccessImporterFromImportSettings):
    """ """

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        settings = super(BuildlicenceImporterFromImportSettings, self).get_importer_settings()

        db_settings = {
            'db_name': 'P_tables.mdb',
        }

        settings.update(db_settings)

        return settings
