# -*- coding: utf-8 -*-

from dateutil import parser

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
        raw_number = self.importer.getData('NUMERO DE DOSSIER', line)
        folder_number = raw_number and int(float(raw_number.replace(',', '.'))) or None
        allowed_divider = folder_number is not None and folder_number % self.divider == self.target

        raw_date = self.importer.getData('DEPOT', line)
        depot_date = parser.parse(raw_date, dayfirst=True)
        allowed_date = not raw_date or depot_date.year < 2014
        allowed_type = self.importer.getData('NORM_UNIK', line) in ['D', 'N', 'M', 'V']

        return allowed_divider and allowed_date and allowed_type
