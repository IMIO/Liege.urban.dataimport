# -*- coding: utf-8 -*-

from imio.urban.dataimport.exceptions import NoObjectToCreateException
from imio.urban.dataimport.factory import BaseFactory
from imio.urban.dataimport.Postgres.mapper import PostgresMapper as Mapper
from imio.urban.dataimport.Postgres.mapper import PostgresFinalMapper as FinalMapper

from plone import api

from Products.CMFPlone.utils import normalizeString

from unidecode import unidecode

import re


#
# LICENCE
#

# factory


class LicenceFactory(BaseFactory):
    def getCreationPlace(self, factory_args):
        foldername = factory_args['portal_type'].lower()
        path = '{}/urban/{}s'.format(self.site.absolute_url_path(), foldername)
        return self.site.restrictedTraverse(path)

# mappers


class IdMapper(Mapper):
    """ """

    def mapId(self, line):
        return self.getData('numetab').replace('/', '_')


class PortalTypeMapper(Mapper):
    """ """
    def mapPortal_type(self, line):
        type_value = self.getData('clasprinc')
        portal_type = None
        if '1' in type_value:
            portal_type = 'EnvClassOne'
        elif '2' in type_value:
            portal_type = 'EnvClassTwo'
        elif '3' in type_value:
            portal_type = 'EnvClassThree'

        if not portal_type:
            self.logError(self, line, 'No portal type found for this type value', {'TYPE value': type_value})
            raise NoObjectToCreateException

        return portal_type


class WorklocationsMapper(Mapper):
    """ """

    def __init__(self, importer, args, table_name=None):
        super(WorklocationsMapper, self).__init__(importer, args, table_name=table_name)
        catalog = api.portal.get_tool('portal_catalog')

        streets_by_code = {}
        street_brains = catalog(portal_type='Street', review_state='enabled', sort_on='id')
        streets = [br.getObject() for br in street_brains]
        for street in streets:
            code = street.getStreetCode()
            if code not in streets_by_code:
                streets_by_code[code] = street
        self.streets_by_code = streets_by_code

        streets = [br.getObject() for br in street_brains]
        for street in streets:
            code = street.getStreetCode()
            if code not in streets_by_code:
                streets_by_code[code] = street

        # handle case of disbaled streets by referencing an active street instead
        disabled_street_brains = catalog(portal_type='Street', review_state='disabled', sort_on='id')
        streets = [br.getObject() for br in disabled_street_brains]
        for street in streets:
            active_street = catalog(portal_type='Street', review_state='enabled', Title=street.getStreetName())
            if len(active_street) != 1:
                continue
            active_street = active_street[0].getObject()
            code = street.getStreetCode()
            if code not in streets_by_code:
                streets_by_code[code] = active_street

        self.streets_by_code = streets_by_code

        portal_urban = self.site.portal_urban
        streets_folders = portal_urban.streets.objectValues()
        self.street_folders = dict(
            [(unidecode(f.Title().decode('utf-8')).upper(), f) for f in streets_folders]
        )

    def mapWorklocations(self, line):
        """ """
        raw_street_code = self.getData('nrue')
        if not raw_street_code:
            return []
        street_code = int(raw_street_code)
        street = self.streets_by_code.get(street_code, None)
        if not street:
            self.logError(
                self,
                line,
                'Unknown street code', {
                    'street_code': street_code,
                    'street_name': self.getData('z_librue'),
                    'street_start': self.getData('z_ravpl'),
                }
            )
            return []
        return [{'street': street.UID(), 'number': ''}]


class ErrorsMapper(FinalMapper):
    def mapDescription(self, line, plone_object):

        line_number = self.importer.current_line
        errors = self.importer.errors.get(line_number, None)
        description = plone_object.Description()

        error_trace = []

        if errors:
            for error in errors:
                data = error.data
                if 'street' in error.message:
                    error_trace.append('<p>adresse : %s, %s %s</p>' % (data['street_code'], data['street_start'], data['street_name']))
            error_trace.append('<br />')
        error_trace = ''.join(error_trace)

        return '%s%s' % (error_trace, description)


#
# PERSON/CORPORATION CONTACT
#

class CorporationFactory(BaseFactory):
    def getPortalType(self, container, **kwargs):
        return 'Corporation'


class ContactIdMapper(Mapper):
    """ """

    def mapId(self, line):
        name = self.getData('firme')
        if not name:
            raise NoObjectToCreateException
        return normalizeString(self.site.portal_urban.generateUniqueId(name))


class ContactStreetMapper(Mapper):
    """ """

    regex = '(.*?)\s*,?\s*(\d.*)\s*\Z'

    def mapStreet(self, line):
        raw_addr = self.getData('expadr')
        match = re.search(self.regex, raw_addr)
        if match:
            street = match.group(1)
            return street

        return raw_addr

    def mapNumber(self, line):
        raw_addr = self.getData('expadr')
        match = re.search(self.regex, raw_addr)
        if match:
            number = match.group(2)
            return number

        return ''
