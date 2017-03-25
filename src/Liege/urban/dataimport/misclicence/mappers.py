# -*- coding: utf-8 -*-

from DateTime import DateTime

from imio.urban.dataimport.csv.mapper import CSVFinalMapper as FinalMapper
from imio.urban.dataimport.csv.mapper import CSVMapper as Mapper
from imio.urban.dataimport.csv.mapper import CSVPostCreationMapper as PostCreationMapper
from imio.urban.dataimport.csv.mapper import MultiLinesSecondaryTableMapper
from imio.urban.dataimport.csv.mapper import SecondaryTableMapper
from imio.urban.dataimport.exceptions import NoObjectToCreateException
from imio.urban.dataimport.factory import BaseFactory
from imio.urban.dataimport.utils import parse_date

from liege.urban.interfaces import IShore
from liege.urban.services import address_service

from plone import api

from Products.CMFPlone.utils import normalizeString

from unidecode import unidecode

from zope.component import queryAdapter

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
        return str(int(float(self.getData('DOSSIER').replace(',', '.'))))


class PortalTypeMapper(Mapper):
    """ """

    def mapPortal_type(self, line):
        type_value = self.getData('Type_trav').upper()
        row = self.getValueMapping('type_map').get(type_value, None)
        portal_type = row and row['portal_type'] or None
        if portal_type == 'UrbanCertificateOne':
            subject = self.getData('Objettrav').lower()
            is_cu2 = self.getData('COLLEGE_DECISION') or 'cu2' in subject or 'cu 2' in subject
            if is_cu2:
                portal_type = 'UrbanCertificateTwo'

        if not portal_type:
            raise NoObjectToCreateException
        return portal_type


class ReferenceMapper(PostCreationMapper):
    """ """

    def mapReference(self, line, plone_object):
        to_shore = queryAdapter(plone_object, IShore)
        shore = to_shore.display()

        type_value = self.getData('Type_trav').upper()
        row = self.getValueMapping('type_map').get(type_value, '')
        abbr = row and row['abreviation'] or None
        if plone_object.portal_type == 'UrbanCertificateTwo':
            abbr = 'CU2'

        ref = '{}/{} {}'.format(abbr, str(int(float(self.getData('DOSSIER').replace(',', '.')))), shore)
        return ref


class CU1SubjectMapper(PostCreationMapper):

    def mapDescription(self, line, plone_object):
        old_description = plone_object.Description()
        if plone_object.portal_type != 'UrbanCertificateOne':
            return old_description

        subject = self.getData('Objettrav')
        description = "<p>objet: {}</p>{}".format(subject, old_description)
        return description


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
        raw_state = self.getData('COLLEGE_DECISION')
        state_mapping = self.getValueMapping('state_map')
        state = state_mapping.get(raw_state, 'accepted')

        workflow_def = workflow_tool.getWorkflowsFor(plone_object)[0]
        workflow_id = workflow_def.getId()
        workflow_state = workflow_tool.getStatusOf(workflow_id, plone_object)
        workflow_state['review_state'] = state
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
        return 'Applicant'

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
        try:
            address = address_factory.create_address(**kwargs)
        except:
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

        raise NoObjectToCreateException

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

#mappers


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
# UrbanEvent inquiry
#


class InquiryEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'copy_of_enquete-publique'


class InquiryExplainationDateMapper(Mapper):

    def mapExplanationstartsdate(self, line):
        date = self.getData('DateBU')
        try:
            date = date and DateTime(parse_date(date)) or None
        except:
            raise NoObjectToCreateException

        licence_id = self.getData('DOSSIER')
        licence_claims = self.importer.mappers['CLAIMANTS']['pre'][0].lines.keys()
        has_claimants = licence_id in licence_claims
        if not date and not has_claimants:
            raise NoObjectToCreateException
        return date


#
# CLAIMANTS
#

# factory


class ClaimantFactory(BaseFactory):
    def getPortalType(self, container, **kwargs):
        return 'Claimant'

# mappers


class ClaimantTableMapper(MultiLinesSecondaryTableMapper):
    """
    Additional claimants mapper
    """


class ClaimantIdMapper(Mapper):
    """ """

    def mapId(self, line):
        name = self.getData('Reclamant')
        if not name:
            raise NoObjectToCreateException

        return normalizeString(self.site.portal_urban.generateUniqueId(name))


class ClaimantTitleMapper(Mapper):
    """ """

    def mapPersontitle(self, line):
        raw_title = self.getData('civilite').lower()
        title_mapping = self.getValueMapping('person_title_map')
        title = title_mapping.get(raw_title, 'notitle')
        return title


class ClaimantStreetMapper(Mapper):
    """ """

    regex = '(.*?)\s*,?\s*(\d.*)\s*\Z'

    def mapStreet(self, line):
        raw_addr = self.getData('adresse')
        match = re.search(self.regex, raw_addr)
        if match:
            street = match.group(1)
            return street

        return raw_addr

    def mapNumber(self, line):
        raw_addr = self.getData('adresse')
        match = re.search(self.regex, raw_addr)
        if match:
            number = match.group(2)
            return number

        return ''


class ClaimantLocalityMapper(Mapper):
    """ """

    regex = '(\d{4,4})\s+(\w.*)'

    def mapZipcode(self, line):
        raw_city = self.getData('CP')
        match = re.search(self.regex, raw_city)
        if match:
            zipcode = match.group(1)
            return zipcode

        return ''

    def mapCity(self, line):
        raw_city = self.getData('CP')
        match = re.search(self.regex, raw_city)
        if match:
            city = match.group(2)
            return city

        return raw_city


class ClaimDateMapper(Mapper):

    def mapClaimdate(self, line):
        date = self.getData('Date_reclam')
        date = date and DateTime(parse_date(date)) or None
        return date


#
# First college  (for FD)
#


class FirstCollegeEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'transmis-2eme-dossier-rw'


class FirstCollegeDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('DATE_COLL_APPREC')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(parse_date(date)) or None
        return date


class FirstCollegeDecisionMapper(Mapper):

    def mapDecision(self, line):

        raw_decision = self.getData('APRREC_ADM').lower()
        if 'déf' in raw_decision:
            return 'defavorable'
        return 'favorable'

#
# FD answer
#


class FDResponseEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'demande-davis-au-fd'


class FDAnswerReceiptDateMapper(Mapper):

    def mapReceiptdate(self, line):
        date = self.getData('DATE_FD')
        date = date and DateTime(parse_date(date)) or None
        return date


class FDOpinionMapper(Mapper):

    def mapExternaldecision(self, line):
        raw_decision = self.getData('AVIS_FD')
        if not raw_decision:
            raise NoObjectToCreateException

        opinion = raw_decision.lower()
        if 'défav' in opinion:
            return 'defavorable'
        return 'favorable'

    def mapOpiniontext(self, line):
        raw_decision = self.getData('AVIS_FD')
        return '<p>%s</p>' % raw_decision


#
# UrbanEvent college final decision
#


class DecisionEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'copy_of_octroi-cu2'


class DecisionDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('DATE_COLL_DECIS')
        date = date and DateTime(parse_date(date)) or None
        return date


class DecisionMapper(Mapper):

    def mapDecision(self, line):
        raw_decision = self.getData('COLLEGE_DECISION')
        if not raw_decision:
            raise NoObjectToCreateException
        if 'déf' in raw_decision.lower():
            return 'defavorable'
        return 'favorable'


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
        licence = self.importer.current_containers_stack[-1]
        raw_task_id = self.getData('numpiece') or '0.0'
        raw_task_id = raw_task_id.replace(',', '.')
        while str(int(float(raw_task_id))) in licence.objectIds():
            raw_task_id = float(raw_task_id) + 1.0
        return str(int(float(raw_task_id)))


class TaskDescriptionMapper(Mapper):
    """ """

    def mapTask_description(self, line):
        foldermanager = self.getData('Gestionnaire')
        foldermanager = foldermanager and '<p>Agent traitant: %s</p>' % foldermanager or ''
        observations = self.getData('Remarques')
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
        except:
            raise NoObjectToCreateException
        return date
