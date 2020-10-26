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
        folder_id = self.importer.getData('DOSSIER', line)
        allowed_divider = False
        if folder_id:
            folder_number = int(float(folder_id.replace(',', '.')))
            allowed_divider = folder_number or True

        allowed_type = self.importer.getData('Type_trav', line) in [
            'DIV', 'DIM', 'MED', 'PLA', 'plainte', 'Plainte', 'DEM', 'amn', 'AMN', 'amnistie', 'AT'
        ]

        return allowed_divider and allowed_type
