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
        folder_id = self.importer.getData('DOSSIER', line)
        allowed_divider = False
        if folder_id:
            folder_number = int(float(folder_id))
            allowed_divider = folder_number > 3 and folder_number % self.divider == self.target

        depot_date = parser.parse(self.importer.getData('DEPOT', line), dayfirst=True)
        allowed_date = not depot_date or depot_date.year >= 2014
        allowed_type = self.importer.getData('Type_trav', line) in ['AP', 'CU', 'DUP', 'PAT']

        return allowed_divider and allowed_date and allowed_type
