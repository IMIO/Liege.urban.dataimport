# -*- coding: utf-8 -*-

from imio.urban.dataimport.browser.controlpanel import ImporterControlPanel
from imio.urban.dataimport.browser.import_panel import ImporterSettings
from imio.urban.dataimport.browser.import_panel import ImporterSettingsForm
from imio.urban.dataimport.access.settings import AccessImporterFromImportSettings


class LiegeImporterSettingsForm(ImporterSettingsForm):
    """ """

class LiegeImporterSettings(ImporterSettings):
    """ """
    form = LiegeImporterSettingsForm


class LiegeImporterControlPanel(ImporterControlPanel):
    """ """
    import_form = LiegeImporterSettings


class LiegeImporterFromImportSettings(AccessImporterFromImportSettings):
    """ """

    def get_importer_settings(self):
        """
        Return the db name to read.
        """
        settings = super(LiegeImporterFromImportSettings, self).get_importer_settings()

        db_settings = {
            'db_name': '',
        }

        settings.update(db_settings)

        return settings
