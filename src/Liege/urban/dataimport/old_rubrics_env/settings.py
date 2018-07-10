# -*- coding: utf-8 -*-

from imio.urban.dataimport.browser.adapter import ImporterFromSettingsForm

from Liege.urban.dataimport.old_rubrics_env.importer import EnvironmentOldRubricsImporter


class EnvironmentOldRubricsImporterFromImportSettings(ImporterFromSettingsForm):
    """ """

    def __init__(self, settings_form, importer_class=EnvironmentOldRubricsImporter):
        """
        """
        super(EnvironmentOldRubricsImporterFromImportSettings, self).__init__(settings_form, importer_class)

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        settings = super(EnvironmentOldRubricsImporterFromImportSettings, self).get_importer_settings()

        db_settings = {
            'table_name': 'tabrub2',
            'key_column': 'num_rubrique2',
        }

        settings.update(db_settings)

        return settings
