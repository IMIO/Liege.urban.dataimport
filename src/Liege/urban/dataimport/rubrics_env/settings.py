# -*- coding: utf-8 -*-

from imio.urban.dataimport.browser.adapter import ImporterFromSettingsForm

from Liege.urban.dataimport.rubrics_env.importer import EnvironmentRubricsImporter


class EnvironmentRubricsImporterFromImportSettings(ImporterFromSettingsForm):
    """ """

    def __init__(self, settings_form, importer_class=EnvironmentRubricsImporter):
        """
        """
        super(EnvironmentRubricsImporterFromImportSettings, self).__init__(settings_form, importer_class)

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        settings = super(EnvironmentRubricsImporterFromImportSettings, self).get_importer_settings()

        db_settings = {
            'table_name': 'tabrub1',
            'key_column': 'rubrique_rubrique1',
        }

        settings.update(db_settings)

        return settings
