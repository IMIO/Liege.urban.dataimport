# -*- coding: utf-8 -*-

from imio.urban.dataimport.browser.adapter import ImporterFromSettingsForm

from Liege.urban.dataimport.environment.importer import EnvironmentLicencesImporter


class EnvironmentLicencesImporterFromImportSettings(ImporterFromSettingsForm):
    """ """

    def __init__(self, settings_form, importer_class=EnvironmentLicencesImporter):
        """
        """
        super(EnvironmentLicencesImporterFromImportSettings, self).__init__(settings_form, importer_class)

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        settings = super(EnvironmentLicencesImporterFromImportSettings, self).get_importer_settings()

        db_settings = {
            'table_name': 'tabaut',
            'key_column': 'autoris',
        }

        settings.update(db_settings)

        return settings
