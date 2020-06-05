# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.mapper import CSVFinalMapper as FinalMapper
from imio.urban.dataimport.csv.mapper import CSVMapper as Mapper
from imio.urban.dataimport.csv.mapper import CSVPostCreationMapper as PostCreationMapper
from imio.urban.dataimport.csv.mapper import SecondaryTableMapper
from imio.urban.dataimport.exceptions import NoObjectToCreateException
from imio.urban.dataimport.factory import BaseFactory

from liege.urban.services import address_service

from plone import api

from Products.CMFPlone.utils import normalizeString

from unidecode import unidecode

import re


#
# Ticket
#

# factory

class TicketFactory(BaseFactory):
    def getCreationPlace(self, factory_args):
        path = '{}/urban/tickets'.format(self.site.absolute_url_path())
        return self.site.restrictedTraverse(path)

    def getPortalType(self, container, **kwargs):
        return 'Ticket'

# mappers


class OldAddressMapper(SecondaryTableMapper):
    """ """


class WorklocationsMapper(Mapper):
    """ """

    def __init__(self, importer, args, csv_filename):
        super(WorklocationsMapper, self).__init__(importer, args, csv_filename=csv_filename)
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
        raw_street_code = self.getData('CODE_RUE')
        if not raw_street_code:
            return []
        street_code = int(raw_street_code)
        street = self.streets_by_code.get(street_code, None)
        street = street or self._create_street()
        return [{'street': street.UID(), 'number': ''}]

    def _create_street(self):
        street_code = self.getData('CODE_RUE')
        street_name = self.getData('RUE')
        street_type = self.getData('PARTICULE')
        city = self.getData('Localite')

        street_folder = self.street_folders.get(city, None)
        if street_folder:
            street_fullname = '{} {}'.format(street_type, street_name)
            street_id = normalizeString(street_fullname)
            if street_id not in street_folder:
                street_id = street_folder.invokeFactory(
                    'Street',
                    id=street_id,
                    StreetName=street_fullname,
                    StreetCode=street_code,
                )
            street = street_folder.get(street_id)
            return street


class OldAddressNumberMapper(PostCreationMapper):
    """ """

    def mapWorklocations(self, line, plone_object):
        """ """
        licence = plone_object
        addr = licence.getWorkLocations()
        if not addr:
            return []

        addr = addr[0]
        num = self.getData('NUM')
        num = num and str(int(float(num.replace(',', '.'))))
        num2 = self.getData('Num2')
        num2 = num2 and ', {}'.format(num2) or ''
        number = '{}{}'.format(num, num2)
        new_addr = {'street': addr['street'], 'number': number}
        return [new_addr]


class CompletionStateMapper(PostCreationMapper):
    def map(self, line, plone_object):
        self.line = line
        workflow_tool = api.portal.get_tool('portal_workflow')

        workflow_def = workflow_tool.getWorkflowsFor(plone_object)[0]
        workflow_id = workflow_def.getId()
        workflow_state = workflow_tool.getStatusOf(workflow_id, plone_object)
        workflow_state['review_state'] = 'ended'
        workflow_tool.setStatusOf(workflow_id, plone_object, workflow_state.copy())


class ErrorsMapper(FinalMapper):
    def mapDescription(self, line, plone_object):

        line_number = self.importer.current_line
        errors = self.importer.errors.get(line_number, None)
        description = plone_object.Description()

        error_trace = []

        if errors:
            for error in errors:
                data = error.data
                if 'inspector' in error.message:
                    error_trace.append('<p>inspecteur : %s</p>' % data['name'])
            error_trace.append('<br />')
        error_trace = ''.join(error_trace)

        return '%s%s' % (error_trace, description)


#
# Address point
#

# factory

class AddressFactory(BaseFactory):
    """ """

    def create(self, kwargs, container, line):
        if not kwargs:
            return None
        address_factory = container.restrictedTraverse('@@create_address')
        try:
            address = address_factory.create_address(**kwargs)
        except Exception:
            self.logError(
                self,
                line,
                'invalid capakey',
                {'capakey': str(kwargs['capakey']), 'address_point': kwargs.get('address_point', None)}
            )
            return None
        return address


class AddressPointMapper(Mapper):

    def map(self, line):
        """
        """
        gid = self.getData('gidptadresse', line)
        session = address_service.new_session()
        address_record = session.query_address_by_gid(gid)
        if address_record:
            return address_record._asdict()

        raise NoObjectToCreateException

#
# PERSON/CORPORATION CONTACT
#

# factory


class TenantFactory(BaseFactory):
    def getPortalType(self, container, **kwargs):
        return 'Tenant'

# factory


class ProprietaryFactory(BaseFactory):
    def getPortalType(self, container, **kwargs):
        return 'Proprietary'

# mappers


class ContactIdMapper(Mapper):
    """ """

    field_name = 'PROPRIETAIRE'

    def mapId(self, line):
        name = self.getData(self.field_name)
        return normalizeString(self.site.portal_urban.generateUniqueId(name))


class ContactAddressTableMapper(SecondaryTableMapper):
    """ """


class ContactAddressMapper(Mapper):
    """ """

    regex_zipcode = '(.*)(\d{4,4})\s+(\S.*)\s*\Z'
    regex_street_1 = '(.*?)\s*,?\s*(\d.*)\s*-?\Z'
    regex_street_2 = '(\d.*?)\s*,?\s*(.*)\s*-?\Z'

    def mapStreet(self, line):
        raw_addr = self.getData('adr_proprio')
        match = re.search(self.regex_zipcode, raw_addr)
        if match:
            street_and_number = match.group(1)
            match = re.search(self.regex_street_1, street_and_number)
            if match:
                return match.group(1)
            match = re.search(self.regex_street_2, street_and_number)
            if match:
                return match.group(2)
            return street_and_number
        return raw_addr

    def mapNumber(self, line):
        raw_addr = self.getData('adr_proprio')
        match = re.search(self.regex_zipcode, raw_addr)
        if match:
            street_and_number = match.group(1)
            match = re.search(self.regex_street_1, street_and_number)
            if match:
                return match.group(2)
            match = re.search(self.regex_street_2, street_and_number)
            if match:
                return match.group(1)
            return ''
        return ''

    def mapZipcode(self, line):
        raw_addr = self.getData('adr_proprio')
        match = re.search(self.regex_zipcode, raw_addr)
        if match:
            zipcode = match.group(2)
            return zipcode
        return ''

    def mapCity(self, line):
        raw_addr = self.getData('adr_proprio')
        match = re.search(self.regex_zipcode, raw_addr)
        if match:
            city = match.group(3)
            return city
        return ''


class TenantIdMapper(ContactIdMapper):
    """ """
    field_name = 'A CHARGE DE'


class Tenant2IdMapper(ContactIdMapper):
    """ """
    field_name = 'Charge 2'


class Tenant3IdMapper(ContactIdMapper):
    """ """
    field_name = 'Charge3'


class TenantAddressMapper(Mapper):
    """ """
    locality_field = 'Localite1'
    address_field = 'Adr1'

    regex_zipcode = '(.*)(\d{4,4})\s+(\S.*)\s*\Z'
    regex_street_1 = '(.*?)\s*,?\s*(\d.*)\s*-?\Z'
    regex_street_2 = '(\d.*?)\s*,?\s*(.*)\s*-?\Z'

    def mapStreet(self, line):
        raw_addr = self.getData(self.address_field)
        match = re.search(self.regex_street_1, raw_addr)
        if match:
            return match.group(1)
        match = re.search(self.regex_street_2, raw_addr)
        if match:
            return match.group(2)
        return raw_addr

    def mapNumber(self, line):
        raw_addr = self.getData(self.address_field)
        match = re.search(self.regex_street_1, raw_addr)
        if match:
            return match.group(2)
        match = re.search(self.regex_street_2, raw_addr)
        if match:
            return match.group(1)
        return ''

    def mapZipcode(self, line):
        raw_addr = self.getData(self.locality_field)
        match = re.search(self.regex_zipcode, raw_addr)
        if match:
            zipcode = match.group(2)
            return zipcode
        return ''

    def mapCity(self, line):
        raw_addr = self.getData(self.locality_field)
        match = re.search(self.regex_zipcode, raw_addr)
        if match:
            city = match.group(3)
            return city
        return ''


class Tenant2AddressMapper(TenantAddressMapper):
    """ """
    locality_field = 'Localite2'
    address_field = 'Adr2'


class Tenant3AddressMapper(TenantAddressMapper):
    """ """
    locality_field = 'Localite3'
    address_field = 'Adr3'
