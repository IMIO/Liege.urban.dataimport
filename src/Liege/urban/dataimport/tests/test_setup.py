# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from Liege.urban.dataimport.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of Liege.urban.dataimport into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if Liege.urban.dataimport is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('Liege.urban.dataimport'))

    def test_uninstall(self):
        """Test if Liege.urban.dataimport is cleanly uninstalled."""
        self.installer.uninstallProducts(['Liege.urban.dataimport'])
        self.assertFalse(self.installer.isProductInstalled('Liege.urban.dataimport'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ILiegeUrbanDataimportLayer is registered."""
        from Liege.urban.dataimport.interfaces import ILiegeUrbanDataimportLayer
        from plone.browserlayer import utils
        self.failUnless(ILiegeUrbanDataimportLayer in utils.registered_layers())
