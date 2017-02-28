# -*- coding: utf-8 -*-

from imio.urban.dataimport.interfaces import IImportSplitter
from imio.urban.dataimport.utils import parse_date

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
        folder_number = int(float(self.importer.getData('Numéro', line)))
        allowed_divider = folder_number % self.divider == self.target
        date = self.importer.getData('Date', line)
        try:
            date = date and parse_date(date) or None
        except:
            return False
        only_year = date.year == 1 and date.day == 1

        return allowed_divider and only_year
