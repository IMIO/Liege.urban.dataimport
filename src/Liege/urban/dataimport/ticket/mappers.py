# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.mapper import CSVFinalMapper as FinalMapper
from imio.urban.dataimport.csv.mapper import CSVMapper as Mapper
from imio.urban.dataimport.csv.mapper import CSVPostCreationMapper as PostCreationMapper
from imio.urban.dataimport.csv.mapper import MultiLinesSecondaryTableMapper
from imio.urban.dataimport.csv.mapper import SecondaryTableMapper
from imio.urban.dataimport.exceptions import NoObjectToCreateException
from imio.urban.dataimport.factory import BaseFactory
from imio.urban.dataimport.utils import parse_date

from liege.urban.services import address_service

from plone import api

from Products.CMFPlone.utils import normalizeString
from Products.urban.interfaces import IGenericLicence

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
        num3 = self.getData('numbisreel')
        num3 = num3 and ', {}'.format(num3) or ''
        number = '{}{}{}'.format(num, num2, num3)
        new_addr = {'street': addr['street'], 'number': number}
        return [new_addr]


class BoundLicencesMapper(PostCreationMapper):
    """ """

    def mapBound_licences(self, line, plone_object):
        self.line = line
        bound_licences = []
        refs_not_found = []
        catalog = api.portal.get_tool('portal_catalog')
        licence_ref = self.getData('Dossiers')
        licence_ref = licence_ref and int(float(licence_ref))
        miscdemand_ref = self.getData('Mise en demeure')
        miscdemand_ref = miscdemand_ref and int(float(miscdemand_ref))
        if licence_ref:
            licence_ref = str(licence_ref)
            brains = catalog(getReference=licence_ref, object_provides=IGenericLicence.__identifier__)
            if len(brains) == 1:
                bound_licences.append(brains[0].UID)
            else:
                refs_not_found.append(licence_ref)
        if miscdemand_ref:
            miscdemand_ref = str(miscdemand_ref)
            brains = catalog(getReference=miscdemand_ref, object_provides=IGenericLicence.__identifier__)
            if len(brains) == 1:
                bound_licences.append(brains[0].UID)
            else:
                refs_not_found.append(miscdemand_ref)
        self.logError(self, line, 'bound_licences', {'refs': refs_not_found})
        return bound_licences


class CompletionStateMapper(PostCreationMapper):
    def map(self, line, plone_object):
        self.line = line
        workflow_tool = api.portal.get_tool('portal_workflow')

        workflow_def = workflow_tool.getWorkflowsFor(plone_object)[0]
        workflow_id = workflow_def.getId()
        workflow_state = workflow_tool.getStatusOf(workflow_id, plone_object)
        workflow_state['review_state'] = 'creation'
        if self.getData('termine'):
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
                if 'bound_licences' in error.message:
                    for ref in data['refs']:
                        error_trace.append('<p>dossier lié non trouvé : %s</p>' % ref)
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


class ProprietaryFactory(BaseFactory):
    def getPortalType(self, container, **kwargs):
        return 'Proprietary'

# mappers


class ContactIdMapper(Mapper):
    """ """

    field_name = 'PROPRIETAIRE'

    def mapId(self, line):
        name = self.getData(self.field_name)
        if not name:
            raise NoObjectToCreateException
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


class ProprietaryIdMapper(ContactIdMapper):
    """ """
    field_name = 'A CHARGE DE'


class Proprietary2IdMapper(ContactIdMapper):
    """ """
    field_name = 'Charge 2'


class Proprietary3IdMapper(ContactIdMapper):
    """ """
    field_name = 'Charge3'


class ProprietaryAddressMapper(Mapper):
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


class Proprietary2AddressMapper(ProprietaryAddressMapper):
    """ """
    locality_field = 'Localite2'
    address_field = 'Adr2'


class Proprietary3AddressMapper(ProprietaryAddressMapper):
    """ """
    locality_field = 'Localite3'
    address_field = 'Adr3'


#
# Tasks (postits)
#

# factory

class TaskFactory(BaseFactory):
    """ """

    def getPortalType(self, container, **kwargs):
        return 'task'


# mappers


class TaskTableMapper(MultiLinesSecondaryTableMapper):
    """ """


class TaskIdMapper(Mapper):
    """ """

    def mapId(self, line):
        return str(int(float(self.getData('numpiece').replace(',', '.'))))


class TaskDescriptionMapper(Mapper):
    """ """

    def mapTask_description(self, line):
        foldermanager = self.getData('Gestionnaire')
        foldermanager = foldermanager and '<p>Agent traitant: %s</p>' % foldermanager or ''
        observations = self.getData('remarques')
        observations = observations and '<p>Remarques: %s</p>' % observations or ''
        from_ = self.getData('Expéditeur')
        from_ = from_ and '<p>Expéditeur: %s</p>' % from_ or ''
        to = self.getData('Destinataire')
        to = to and '<p>Expéditeur: %s</p>' % to or ''
        expedition = self.getData('Expédition')
        expedition = expedition and '<p>Expédition: %s</p>' % expedition or ''

        description = '{}{}{}{}{}'.format(foldermanager, observations, from_, to, expedition)
        return description.decode('utf-8')


class TaskDateMapper(Mapper):
    """ """

    def mapDue_date(self, line):
        date = self.getData('Date')
        try:
            date = date and parse_date(date) or None
        except Exception:
            raise NoObjectToCreateException
        return date
