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
        folder_number = int(float(self.importer.getData('NUMERO DE DOSSIER', line)))
        allowed_divider = folder_number % self.divider == self.target

        depot_date = parser.parse(self.importer.getData('DEPOT', line))
        allowed_date = depot_date.year < 2014
        allowed_type = self.importer.getData('NORM_UNIK', line) in ['D', 'N', 'M', 'V']

        return allowed_divider and allowed_date and allowed_type
