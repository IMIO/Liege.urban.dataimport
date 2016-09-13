# -*- coding: utf-8 -*-

from imio.urban.dataimport.browser.controlpanel import ImporterControlPanel
from imio.urban.dataimport.browser.import_panel import ImporterSettings
from imio.urban.dataimport.browser.import_panel import ImporterSettingsForm


class LiegeImporterSettingsForm(ImporterSettingsForm):
    """ """


class LiegeImporterSettings(ImporterSettings):
    """ """
    form = LiegeImporterSettingsForm


class LiegeImporterControlPanel(ImporterControlPanel):
    """ """
    import_form = LiegeImporterSettings
