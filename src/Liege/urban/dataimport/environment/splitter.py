# -*- coding: utf-8 -*-

from imio.urban.dataimport.interfaces import IImportSplitter

from zope.interface import implements


class EnvironmentImportSplitter(object):
    """
    """
    implements(IImportSplitter)

    def __init__(self, importer):
        self.importer = importer
        self.divider = importer.split_division_range
        self.target = importer.split_division_target

    def allow(self, line):
        """ """
        allowed_type = self.importer.getData('nature', line) in ['PU']
        # allowed_type = self.importer.getData('autoris', line) in ['1/11C38']
        # allowed_type = True

        return allowed_type
