# -*- coding: utf-8 -*-

from imio.urban.dataimport.interfaces import IImportSplitter
from imio.urban.dataimport.utils import parse_date

from plone import api

from zope.interface import implements


class LiegeImportSplitter(object):
    """
    """
    implements(IImportSplitter)

    def __init__(self, importer):
        self.importer = importer
        self.divider = importer.split_division_range
        self.target = importer.split_division_target
        self.disabled_streets = self.get_disabled_streets()

    def get_disabled_streets(self):
        """
        """
        street_mapper = [m for m in self.importer.mappers['LICENCE']['pre'] if 'StreetTableMapper' in str(m)][0]
        catalog = api.portal.get_tool('portal_catalog')
        disabled_streets = catalog(portal_type='Street', review_state='disabled')
        disabled_INS_codes = set([str(b.getObject().getStreetCode()) for b in disabled_streets])
        enabled_streets = catalog(portal_type='Street', review_state='enabled')
        enabled_INS_codes = set([str(b.getObject().getStreetCode()) for b in enabled_streets])
        disabled_ids = [k for k, v in street_mapper.lines.iteritems() if v[0][1] in disabled_INS_codes and v[0][1] not in enabled_INS_codes]
        return disabled_ids

    def allow(self, line):
        """ """
        street_number = self.importer.getData('ref_rue', line)
        if street_number in self.disabled_streets:
            return True
        return False
        folder_number = int(float(self.importer.getData('Numéro', line)))
        allowed_divider = folder_number % self.divider == self.target
        date = self.importer.getData('Date', line)
        try:
            date = date and parse_date(date) or None
        except:
            return False
        only_year = date.year == 1 and date.day == 1

        return allowed_divider and only_year
