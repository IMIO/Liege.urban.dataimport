# -*- coding: utf-8 -*-

from imio.urban.dataimport.interfaces import IImportSplitter

from zope.interface import implements


class LiegeImportSplitter(object):
    """
    """
    implements(IImportSplitter)

    def __init__(self, importer):
        self.importer = importer
        self.divider = importer.split_division_range
        self.target = importer.split_division_target

    def allow(self, line):
        """ """
        return True
