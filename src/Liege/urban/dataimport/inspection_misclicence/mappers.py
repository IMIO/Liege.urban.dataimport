# -*- coding: utf-8 -*-

from DateTime import DateTime

from imio.urban.dataimport.csv.mapper import CSVFinalMapper as FinalMapper
from imio.urban.dataimport.csv.mapper import CSVMapper as Mapper
from imio.urban.dataimport.csv.mapper import CSVPostCreationMapper as PostCreationMapper
from imio.urban.dataimport.csv.mapper import MultiLinesSecondaryTableMapper
from imio.urban.dataimport.csv.mapper import MultivaluedFieldSecondaryTableMapper
from imio.urban.dataimport.csv.mapper import SecondaryTableMapper
from imio.urban.dataimport.exceptions import NoObjectToCreateException
from imio.urban.dataimport.factory import BaseFactory
from imio.urban.dataimport.utils import parse_date

from liege.urban.services import address_service

from plone import api

from Products.CMFPlone.utils import normalizeString

from unidecode import unidecode

import re


#
# LICENCE
#

# factory


class LicenceFactory(BaseFactory, Mapper):
    """
    Override the factory to create either an inspection licence or an urbanevent if the inspection licence
    already exists.
    """
    def __init__(self, *args, **kwargs):
        super(LicenceFactory, self).__init__(*args, **kwargs)
        urban_tool = api.portal.get_tool('portal_urban')
        config = urban_tool.inspection
        eventtype_id = 'followup-access'
        self.eventtype_uid = getattr(config.urbaneventtypes, eventtype_id).UID()
        self.sources = []
        self.destinations = []
        catalog = api.portal.get_tool('portal_catalog')
        all_inspections = catalog(portal_type='Inspection')
        self.inspections_by_capakeys = {}
        for inspection_brain in all_inspections:
            for capakey in inspection_brain.parcelInfosIndex:
                if capakey in self.inspections_by_capakeys:
                    self.inspections_by_capakeys[capakey].append(inspection_brain)
                else:
                    self.inspections_by_capakeys[capakey] = [inspection_brain]

    def create(self, kwargs, container=None, line=None):
        self.line = line
        session = address_service.new_session()
        all_pt_adresses = [kwargs['pt_address']] + kwargs.get('additional_ptadress', [])
        for pt_address in all_pt_adresses:
            address_record = session.query_address_by_gid(pt_address)
            if not address_record:
                continue
            existing_inspections = self.inspections_by_capakeys.get(address_record.capakey, None)
            if existing_inspections:
                session.close()
                existing_inspections = sorted(existing_inspections, key=lambda x: x.getReference, reverse=True)
                inspection = existing_inspections[0].getObject()
                self.importer.recursiveImportObjects('TASKS', [], self.line, [inspection])
                urban_event = inspection.createUrbanEvent(self.eventtype_uid)

                type_trav = self.getData('Type_trav')
                subject = self.getData('Objettrav')
                num = self.getData('DOSSIER')
                title = '{} - {} - {}'.format(num, type_trav, subject)
                urban_event.setTitle(title)

                date = self.getData('DEPOT')
                date = date and DateTime(parse_date(date)) or None
                urban_event.setEventDate(date)

                persontitle = self.getData('QUALITE')
                applicant = self.getData('NOM DU DEMANDEUR')
                tel = self.getData('TELDEMANDEUR')
                address = self.getData('ADRESSE DEMANDEUR')
                zipcode = self.getData('CODE POSTAL22')
                locality = self.getData('LOCALITE22')
                description = '{} {}\n{} {} {}\n{}'.format(
                    persontitle, applicant, address, zipcode, locality, tel
                )
                urban_event.setMisc_description(description)
                old_AD_refs = inspection.getFormal_notice_old_reference()
                new_AD_refs = old_AD_refs and '{} - {}'.format(old_AD_refs, num) or num
                inspection.setFormal_notice_old_reference(new_AD_refs)
                inspection.updateTitle()
                urban_event.reindexObject()
                return None

        session.close()
        return super(LicenceFactory, self).create(kwargs, container=container, line=line)

    def getCreationPlace(self, factory_args):
        foldername = factory_args['portal_type'].lower()
        path = '{}/urban/{}s'.format(self.site.absolute_url_path(), foldername)
        return self.site.restrictedTraverse(path)

# mappers


class IdMapper(Mapper):
    """ """

    def mapId(self, line):
        return str(int((self.getData('DOSSIER') or '0').replace(',', '.')))


class PortalTypeMapper(Mapper):
    """ """

    def mapPortal_type(self, line):
        return 'Inspection'


class ReferenceMapper(PostCreationMapper):
    """ """

    def mapReference(self, line, plone_object):
        abbr = 'IB'
        ref = '{}/{}'.format(abbr, str(int(float(self.getData('DOSSIER').replace(',', '.')))))
        return ref


class InspectionContextMapper(Mapper):
    """ """

    def mapInspection_context(self, line):
        trav_type = self.getData('Type_trav')
        context_mapping = self.getValueMapping('inspection_context')
        inspection_context = context_mapping.get(trav_type, None)
        return inspection_context


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

        # handle case of disabled streets by referencing an active street instead
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
                if 'streets' in error.message:
                    error_trace.append('<p>adresse : %s</p>' % data['address'])
                elif 'annoncedDelay' in error.message:
                    error_trace.append('<p>Délai annoncé : %s</p>' % (data['delay']))
                elif 'solicitOpinionsTo' in error.message:
                    error_trace.append('<p>Avis de service non sélectionné: %s</p>' % (data['name']))
                elif 'workflow state' in error.message:
                    error_trace.append('<p>état final: %s</p>' % (data['state']))
                elif 'invalid capakey' in error.message:
                    ptid = data['address_point']
                    pt_msg = ptid and ' (point adresse %s)' % ptid or ''
                    msg = '<p>capakey invalide %s%s</p>' % (data['capakey'], pt_msg)
                    error_trace.append(msg)
            error_trace.append('<br />')
        error_trace = ''.join(error_trace)

        return '%s%s' % (error_trace, description)

#
# PERSON/CORPORATION CONTACT
#

# factory


class ContactFactory(BaseFactory):
    def getPortalType(self, container, **kwargs):
        return 'Proprietary'

    def objectAlreadyExists(self, object_args, container):
        contact = [obj for obj in container.objectValues() if obj.portal_type == 'Applicant']
        return contact and contact[0] or None


class CorporationFactory(BaseFactory):
    def getPortalType(self, container, **kwargs):
        return 'Corporation'

    def objectAlreadyExists(self, object_args, container):
        contact = [obj for obj in container.objectValues() if obj.portal_type == 'Corporation']
        return contact and contact[0] or None

# mappers


class ContactIdMapper(Mapper):
    """ """

    def mapId(self, line):
        raw_name = self.getData('NOM DU DEMANDEUR')
        raw_title = self.getData('QUALITE')
        name = raw_name or raw_title

        if not name:
            raise NoObjectToCreateException

        return normalizeString(self.site.portal_urban.generateUniqueId(name))


class ContactStreetMapper(Mapper):
    """ """

    regex = '(.*?)\s*,?\s*(\d.*)\s*\Z'

    def mapStreet(self, line):
        raw_addr = self.getData('ADRESSE DEMANDEUR')
        match = re.search(self.regex, raw_addr)
        if match:
            street = match.group(1)
            return street

        return raw_addr

    def mapNumber(self, line):
        raw_addr = self.getData('ADRESSE DEMANDEUR')
        match = re.search(self.regex, raw_addr)
        if match:
            number = match.group(2)
            return number

        return ''


class LocalityMapper(Mapper):
    """ """

    regex = '(\d{4,4})\s+(\w.*)'

    def mapZipcode(self, line):
        raw_zipcode = self.getData('CODE POSTAL22')
        if raw_zipcode:
            return str(int(float(raw_zipcode.replace(',', '.'))))
        return ''

    def mapCity(self, line):
        raw_city = self.getData('LOCALITE22')
        match = re.search(self.regex, raw_city)
        if match:
            city = match.group(2)
            return city

        return raw_city


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
        kwargs['id'] = normalizeString(self.site.portal_urban.generateUniqueId(kwargs['capakey']))
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
        if gid and gid != '0':
            session = address_service.new_session()
            address_record = session.query_address_by_gid(gid)
            session.close()
            if address_record:
                return address_record._asdict()

        # in case there's no address point try to use the capakey
        capakey = self.getData('capakey', line)
        if capakey:  # dont use capakey when idptadresse is 0 because its always a wrong one!
            address_args = {'capakey': capakey}
            licence = self.importer.current_containers_stack[-1]
            addr = licence.getWorkLocations()
            if addr:
                addr = addr[0]
                address_args['street_number'] = addr['number']
                catalog = api.portal.get_tool('portal_catalog')
                street_brains = catalog(UID=addr['street'])
                if street_brains:
                    street = street_brains[0].getObject()
                    address_args['street_name'] = street.getStreetName()
                    address_args['street_code'] = street.getStreetCode()

            return address_args
        return None


class MiscInspectionAddressPointTableMapper(MultivaluedFieldSecondaryTableMapper):
    """ """

    def mapAdditional_ptadress(self, line):
        self.csv_filename = self.secondary_table
        return [self.getData('gidptadresse', line)]


class InspectionAddressPointTableMapper(MultiLinesSecondaryTableMapper):
    """ """


class AdditionalAddressPointMapper(Mapper):

    def map(self, line):
        """
        """
        gid = self.getData('gidptadresse', line)
        session = address_service.new_session()
        address_record = session.query_address_by_gid(gid)
        session.close()
        if address_record:
            return address_record._asdict()
        return {}

#
# UrbanEvent base
#

# factory


class UrbanEventFactory(BaseFactory):
    """ """

    def create(self, kwargs, container, line):
        eventtype_uid = kwargs.pop('eventtype')
        if 'eventDate' not in kwargs:
            kwargs['eventDate'] = None
        urban_event = container.createUrbanEvent(eventtype_uid, **kwargs)
        return urban_event

# mappers


class EventTypeMapper(Mapper):
    """ """

    eventtype_id = ''  # to override

    def mapEventtype(self, line):
        if not self.eventtype_id:
            return
        licence = self.importer.current_containers_stack[-1]
        urban_tool = api.portal.get_tool('portal_urban')
        config = urban_tool.getUrbanConfig(licence)

        event_id_mapping = self.getValueMapping('eventtype_id_map')[licence.portal_type]
        eventtype_id = event_id_mapping.get(self.eventtype_id, self.eventtype_id)

        return getattr(config.urbaneventtypes, eventtype_id).UID()


class EventCompletionStateMapper(PostCreationMapper):
    def map(self, line, plone_object):
        self.line = line
        workflow_tool = api.portal.get_tool('portal_workflow')

        workflow_def = workflow_tool.getWorkflowsFor(plone_object)[0]
        workflow_id = workflow_def.getId()
        workflow_state = workflow_tool.getStatusOf(workflow_id, plone_object)
        workflow_state['review_state'] = 'closed'
        workflow_tool.setStatusOf(workflow_id, plone_object, workflow_state.copy())


#
# UrbanEvent deposit
#


class DepositEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'deposit_event'


class DepositDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('DEPOT')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(parse_date(date)) or None
        return date

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


class TaskTitleMapper(Mapper):
    """ """

    def mapTitle(self, line):
        ref = self.getData('dossier')
        subject = self.getData('Objet')
        return '{} - {}'.format(ref, subject)


class TaskIdMapper(Mapper):
    """ """

    def mapId(self, line):
        licence_id = self.getData('dossier')
        raw_task_id = self.getData('numpiece') or '0.0'
        return '{}_{}'.format(licence_id, raw_task_id)


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
        to = to and '<p>Destinataire: %s</p>' % to or ''
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
