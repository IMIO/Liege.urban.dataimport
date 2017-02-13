# -*- coding: utf-8 -*-

from DateTime import DateTime
from datetime import datetime

from imio.urban.dataimport.access.mapper import AccessFinalMapper as FinalMapper
from imio.urban.dataimport.access.mapper import AccessMapper as Mapper
from imio.urban.dataimport.access.mapper import AccessPostCreationMapper as PostCreationMapper
from imio.urban.dataimport.access.mapper import MultiLinesSecondaryTableMapper
from imio.urban.dataimport.access.mapper import SecondaryTableMapper
from imio.urban.dataimport.access.mapper import MultivaluedFieldSecondaryTableMapper
from imio.urban.dataimport.exceptions import NoObjectToCreateException
from imio.urban.dataimport.factory import BaseFactory

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


class ReferenceMapper(PostCreationMapper):
    def mapReference(self, line, plone_object):
        to_shore = queryAdapter(plone_object, IShore)
        shore = to_shore.display()

        type_value = self.getData('NORM_UNIK').upper()
        row = self.getValueMapping('type_map').get(type_value, '')
        abbr = row and row['abreviation'] or None

        ref = '{}/{} {}'.format(abbr, self.getData('NUMDOSSIERBKP'), shore)
        return ref


class TypeAndCategoryMapper(Mapper):
    """ """
    def mapPortal_type(self, line):
        type_value = self.getData('NORM_UNIK').upper()
        row = self.getValueMapping('type_map').get(type_value, None)
        portal_type = row and row['portal_type'] or None
        if not portal_type:
            self.logError(self, line, 'No portal type found for this type value', {'TYPE value': type_value})
            raise NoObjectToCreateException
        return portal_type

    def mapFoldercategory(self, line):
        type_value = self.getData('NORM_UNIK').upper()
        foldercategory = self.getValueMapping('type_map')[type_value]['foldercategory']
        return foldercategory


class FolderCategoryMapper(Mapper):
    """ """
    def mapFoldercategorytownship(self, line):
        return self.getData('CODE NAT TRAVAUX')


class AnnoncedDelayMapper (Mapper):
    """ """

    def mapAnnonceddelay(self, line):
        raw_delay = self.getData('Délai')
        if raw_delay not in ['30', '70', '75', '115', '230']:
            if raw_delay:
                self.logError(self, line, 'annoncedDelay', {'delay': raw_delay})
            return 'inconnu'
        else:
            return raw_delay + 'j'


class OldAddressMapper(SecondaryTableMapper):
    """ """


class WorklocationsMapper(Mapper):
    """ """

    def __init__(self, importer, args, table_name):
        super(WorklocationsMapper, self).__init__(importer, args, table_name)
        catalog = api.portal.get_tool('portal_catalog')

        streets_by_code = {}
        street_brains = catalog(portal_type='Street', review_state='enabled', sort_on='id')
        streets = [br.getObject() for br in street_brains]
        for street in streets:
            code = street.getStreetCode()
            if code not in streets_by_code:
                streets_by_code[code] = street
        self.streets_by_code = streets_by_code

        portal_urban = self.site.portal_urban
        streets_folders = portal_urban.streets.objectValues()
        self.street_folders = dict(
            [(unidecode(f.Title().decode('utf-8')).upper(), f) for f in streets_folders]
        )

    def mapWorklocations(self, line):
        """ """
        street_code = int(self.getData('CODE_RUE'))
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
        num = num and str(int(float(num)))
        num2 = self.getData('Num2')
        num2 = num2 and ', {}'.format(num2) or ''
        number = '{}{}'.format(num, num2)
        new_addr = {'street': addr['street'], 'number': number}
        return [new_addr]


class ArchitectMapper(Mapper):
    """ """

    def mapArchitects(self, line):
        raw_archi_id = self.getData('NUMARCHITECTE')
        archi_id = raw_archi_id and str(int(float(raw_archi_id))) or ''
        archi = getattr(self.site.urban.architects, archi_id, None)
        return archi


class PEBMapper(Mapper):
    """ """

    def mapPebdetails(self, line):
        """ """
        details = []

        columns = (
            'PEB_dateengag',
            'PEB_engag_comm',
            'PEB_datefinal',
            'PEB_final_comm',
            'PEB_RW',
            'PEB_dateEngageDem',
            'PEB_dateEngageDemComm',
        ),

        for col_name in columns:
            col_value = self.getData('PEB_dateEngageDem')
            if col_value:
                details.append('<p>%s</p>' % col_value)

        return ''.join(details)


class SolicitOpinionsMapper(MultivaluedFieldSecondaryTableMapper):
    """
    """

    def mapSolicitopinionsto(self, line):
        urban_tool = api.portal.get_tool('portal_urban')
        type_value = self.getData('NORM_UNIK', self.main_line).upper()
        portal_type = self.getValueMapping('type_map')[type_value]['portal_type']
        if not portal_type:
            raise NoObjectToCreateException
        folderconfig = getattr(urban_tool, portal_type.lower())
        event_types_path = '/'.join(folderconfig.urbaneventtypes.getPhysicalPath())
        service_name = line[1].replace('.', '').replace('(', ' ').replace(')', ' ')
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(Title=service_name, portal_type='OpinionRequestEventType', path=event_types_path)
        if len(brains) == 1:
            return [brains[0].getObject().id]
        self.logError(self, line, 'solicitOpinionsTo', {'name': line[1]})
        return []


class InquiryDetailsMapper(SecondaryTableMapper):
    """
    Additional claimants mapper
    """


class ArticleTextMapper(Mapper):
    """ """

    def mapInvestigationarticlestext(self, line):
        return '<p>{}</p>'.format(self.getData('carac1', line))


class HabitationMapper(Mapper):
    """ """

    def mapNoapplication(self, line):
        habitation_nbr = self.getData('NB_LOG')
        habitation_nbr = habitation_nbr and int(habitation_nbr) or 0
        return not bool(habitation_nbr)

    def mapAdditionalhabitationsasked(self, line):
        habitation_nbr = self.getData('NB_LOG')
        if habitation_nbr and habitation_nbr != '0':
            return int(habitation_nbr)
        return ''

    def mapAdditionalhabitationsgiven(self, line):
        habitation_nbr = self.getData('NB_LOG_AUTORISES')
        if habitation_nbr and habitation_nbr != '0':
            return int(habitation_nbr)
        return ''

    def mapHabitationsafterlicence(self, line):
        habitation_nbr = self.getData('NB_LOG_DECLARES')
        if habitation_nbr and habitation_nbr != '0':
            return int(habitation_nbr)
        return ''


class DescriptionMapper(Mapper):
    """ """

    def mapDescription(self, line):
        description = []

        plans = self.getData('NOMBRE DE PLANS')
        if plans:
            description.append('<p>Nombre de plans: %s</p>' % str(int(float(plans))))

        report = self.getData('Ajourne2')
        if report:
            description.append('<p>Ajourné: %s</p>' % report)

        description = ''.join(description)
        return description


class CompletionStateMapper(PostCreationMapper):
    def map(self, line, plone_object):
        self.line = line
        workflow_tool = api.portal.get_tool('portal_workflow')
        raw_state = self.getData('COLLDECISION').lower()
        if 'sans' in raw_state and 'suite' in raw_state:
            raw_state = 'sans suite'
        state_mapping = self.getValueMapping('state_map')
        state = state_mapping.get(raw_state, '')
        if not state:
            self.logError(
                self,
                line,
                'unknown workflow state',
                {'state': raw_state}
            )
            return

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


class CorporationFactory(BaseFactory):
    def getPortalType(self, container, **kwargs):
        return 'Corporation'

# mappers


class ContactIdMapper(Mapper):
    """ """

    def mapId(self, line):
        raw_name = self.getData('NOM DU DEMANDEUR')
        raw_title = self.getData('QUALITE')
        if not raw_title:
            raise NoObjectToCreateException

        name = raw_name or raw_title
        return normalizeString(self.site.portal_urban.generateUniqueId(name))


class CorporationIdMapper(Mapper):
    """ """

    def mapId(self, line):
        denomination = self.getData('NOM DU DEMANDEUR')
        legal_form = self.getData('QUALITE')
        if not denomination and not legal_form:
            raise NoObjectToCreateException

        name = denomination or legal_form
        return normalizeString(self.site.portal_urban.generateUniqueId(name))


class ContactTitleMapper(Mapper):
    """ """

    def mapPersontitle(self, line):
        raw_title = self.getData('QUALITE').lower()
        title_mapping = self.getValueMapping('person_title_map')
        title = title_mapping.get(raw_title, None)
        if not title:
            raise NoObjectToCreateException
        return title


class ContactNameMapper(Mapper):
    """ """

    regex_1 = '([A-Z]+-?[A-Z]+)\s+([A-Z][a-z]+-?[a-z]*)\s*\Z'
    regex_2 = '([A-Z][a-z]+-?[a-z]*)\s+([A-Z]+-?[A-Z]+)\s*\Z'

    def mapName1(self, line):
        raw_name = self.getData('NOM DU DEMANDEUR')
        match = re.search(self.regex_1, raw_name)
        if match:
            name1 = match.group(1)
            return name1

        match = re.search(self.regex_2, raw_name)
        if match:
            name1 = match.group(2)
            return name1

        return raw_name

    def mapName2(self, line):
        raw_name = self.getData('NOM DU DEMANDEUR')
        match = re.search(self.regex_1, raw_name)
        if match:
            name2 = match.group(2)
            return name2

        match = re.search(self.regex_2, raw_name)
        if match:
            name2 = match.group(1)
            return name2

        return ''


class CorporationNameMapper(Mapper):
    """ """

    def mapDenomination(self, line):
        denomination = self.getData('NOM DU DEMANDEUR')
        legal_form = self.getData('QUALITE')

        if not denomination and legal_form:
            return legal_form

        return denomination

    def mapLegalform(self, line):
        denomination = self.getData('NOM DU DEMANDEUR')
        legal_form = self.getData('QUALITE')

        if not denomination and legal_form:
            return ''

        return legal_form


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
        raw_city = self.getData('CP LOCALITE DEM')
        match = re.search(self.regex, raw_city)
        if match:
            zipcode = match.group(1)
            return zipcode

        return ''

    def mapCity(self, line):
        raw_city = self.getData('CP LOCALITE DEM')
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
        session = address_service.new_session()
        address_record = session.query_address_by_gid(gid)
        if address_record:
            return address_record._asdict()

        # in case there's no address point try to use the capakey
        capakey = self.getData('CAPAKEY', line)
        if capakey:
            return {'capakey': capakey}

        raise NoObjectToCreateException


class ParcelsMapper(MultiLinesSecondaryTableMapper):
    """
     Parcels table join mapper
    """


class CapakeyMapper(Mapper):
    """
    """

    def mapCapakey(self, line):
        """ """
        raw_capakey = self.getData('CAPAKEY')
        if len(raw_capakey) == 17:
            return raw_capakey
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
        date = date and DateTime(date) or None
        return date


#
# Second UrbanEvent deposit
#


class SecondDepositEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'second_deposit_event'


class SecondDepositDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('Date_accuse2')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(date) or None
        return date


#
# UrbanEvent inquiry
#


class InquiryEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'enquete-publique'


class InquiryStartDateMapper(Mapper):

    def mapInvestigationstart(self, line):
        date = self.getData('DébutPUB')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(date) or None
        return date


class InquiryEndDateMapper(Mapper):

    def mapInvestigationend(self, line):
        date = self.getData('FinPUB')
        date = date and DateTime(date) or None
        return date


class InquiryExplainationDateMapper(Mapper):

    def mapExplanationstartsdate(self, line):
        date = self.getData('DateBU')
        date = date and DateTime(date) or None
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


class ClaimantNameMapper(Mapper):
    """ """

    regex_1 = '([A-Z]+-?[A-Z]+)\s+([A-Z][a-z]+-?[a-z]*)\s*\Z'
    regex_2 = '([A-Z][a-z]+-?[a-z]*)\s+([A-Z]+-?[A-Z]+)\s*\Z'

    def mapName1(self, line):
        raw_name = self.getData('Reclamant')
        match = re.search(self.regex_1, raw_name)
        if match:
            name1 = match.group(1)
            return name1

        match = re.search(self.regex_2, raw_name)
        if match:
            name1 = match.group(2)
            return name1

        return raw_name

    def mapName2(self, line):
        raw_name = self.getData('Reclamant')
        match = re.search(self.regex_1, raw_name)
        if match:
            name2 = match.group(2)
            return name2

        match = re.search(self.regex_2, raw_name)
        if match:
            name2 = match.group(1)
            return name2

        return ''


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
        date = date and DateTime(date) or None
        return date


#
# Opinion request urban events
#

# factory


class OpinionRequestEventFactory(UrbanEventFactory):

    def create(self, kwargs, container, line):
        if not kwargs:
            return None
        title = kwargs.pop('Title')
        if kwargs['eventtype']:
            return super(OpinionRequestEventFactory, self).create(kwargs, container, line)

        kwargs['eventtype'] = 'config-opinion-request'
        opinion_event = super(OpinionRequestEventFactory, self).create(kwargs, container, line)
        opinion_event.setTitle(title)

        return opinion_event

# mappers


class OpinionRequestMapper(MultiLinesSecondaryTableMapper):
    """ """


class OpinionEventTypeMapper(Mapper):
    """ """

    def mapEventtype(self, line):
        licence = self.importer.current_containers_stack[-1]
        config = licence.getLicenceConfig()
        event_types_path = '/'.join(config.urbaneventtypes.getPhysicalPath())
        service_name = self.getData('Nom_service').replace('.', '').replace('(', ' ').replace(')', ' ')
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(Title=service_name, portal_type='OpinionRequestEventType', path=event_types_path)
        if len(brains) == 1:
            return brains[0].getObject().id
        return None


class OpinionIdMapper(Mapper):

    def mapId(self, line):
        return normalizeString(self.getData('Nom_service'))


class OpinionTitleMapper(Mapper):

    def mapTitle(self, line):
        return 'Demande d\'avis (%s)' % self.getData('Nom_service')


class OpinionTransmitDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('Date demande')
        date = date and DateTime(date) or None
        return date

    def mapTransmitdate(self, line):
        date = self.getData('Date demande')
        date = date and DateTime(date) or None
        return date


class OpinionReceiptDateMapper(Mapper):

    def mapReceiptdate(self, line):
        date = self.getData('Date réception')
        date = date and DateTime(date) or None
        return date


class OpinionMapper(Mapper):

    def mapExternaldecision(self, line):
        raw_decision = self.getData('Service_avis')
        decision = self.getValueMapping('externaldecisions_map').get(raw_decision, 'non-determine')
        return decision

    def mapOpiniontext(self, line):
        raw_decision = self.getData('Service_avis')
        decision = self.getValueMapping('externaldecisions_map').get(raw_decision, None)
        if decision:
            return '<p></p>'
        return '<p>%s</p>' % raw_decision


#
# First college  (for FD)
#


class FirstCollegeEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'transmis-2eme-dossier-rw'


class FirstCollegeDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('College2')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(date) or None
        return date


class FirstCollegeDecisionMapper(Mapper):

    def mapDecision(self, line):
        ajourne = self.getData('Ajourne2')
        if ajourne:
            return []

        raw_decision = self.getData('College/Fav/Def').lower()
        if 'def' in raw_decision:
            return 'defavorable'
        return 'favorable'

#
# Second college  (for FD)
#


class SecondCollegeEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'transmis-2eme-dossier-rw'


class SecondCollegeDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('College3')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(date) or None
        return date


class SecondCollegeDecisionMapper(Mapper):

    def mapDecision(self, line):
        raw_decision = self.getData('College/Fav/Def2')
        if 'def' in raw_decision:
            return 'defavorable'
        return 'favorable'

#
# FD answer
#


class FDResponseEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'transmis-2eme-dossier-rw'


class FDTransmitDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('UP2')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(date) or None
        return date


class FDAnswerReceiptDateMapper(Mapper):

    def mapReceiptdate(self, line):
        date = self.getData('UP3')
        date = date and DateTime(date) or None
        return date


class FDOpinionMapper(Mapper):

    def mapExternaldecision(self, line):
        raw_decision = self.getData('Avis')
        opinion = raw_decision.lower()
        if 'rép' in opinion or 'défau' in opinion:
            return 'favorable-defaut'
        elif 'défav' in opinion:
            return 'defavorable'
        elif 'favorable cond' in opinion or 'fav cond' in opinion:
            return 'favorable-conditionnel'
        elif opinion == 'fav' or opinion == 'fav.' or opinion == 'favorable':
            return 'favorable'

        self.logError(
            self,
            line,
            'unknown FD opinion',
            {'opinion': raw_decision}
        )
        return 'non-determine'

    def mapOpiniontext(self, line):
        raw_decision = self.getData('Avis')
        return '<p>%s</p>' % raw_decision


#
# UrbanEvent college final decision
#


class DecisionEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'delivrance-du-permis-octroi-ou-refus'


class DecisionEventTitleMapper(PostCreationMapper):

    def mapTitle(self, line, plone_object):
        old_title = plone_object.Title()
        decision_taker = self.getData('DecisionFinaleUP')
        if decision_taker:
            new_title = '{} ({})'.format(old_title, decision_taker)
            return new_title
        else:
            return old_title


class NotificationDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('notification')
        date = date and DateTime(date) or None
        return date


class DeclarationNotificationDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('notification')
        date = date and DateTime(date) or None
        if not date:
            raise NoObjectToCreateException
        return date


class DecisionDateMapper(Mapper):

    def mapDecisiondate(self, line):
        date = self.getData('COLLDEFINITIF1')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(date) or None
        return date


class DeclarationDecisionDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('COLLDEFINITIF1')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(date) or None
        return date


class DecisionMapper(Mapper):

    def mapDecision(self, line):
        raw_decision = self.getData('COLLDECISION')
        if 'autorisé' in raw_decision.lower():
            return 'favorable'
        return 'defavorable'


#
# UrbanEvent notification
#


class NotificationEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'transmis-decision'


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
        return str(int(float(self.getData('numpiece'))))


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
        date = date and datetime.strptime(date, '%x %X') or None
        return date


#
# Archive Task (postit)
#


class ArchiveTaskTitle(Mapper):
    """ """

    def mapTitle(self, line):
        return 'Archivage'


class ArchiveTaskIdMapper(Mapper):
    """ """

    def mapId(self, line):
        return 'archivage'


class ArchiveTaskDateMapper(Mapper):
    """ """

    def mapDue_date(self, line):
        date = self.getData('ARCH/Cad')
        if not date:
            raise NoObjectToCreateException
        date = date and datetime.strptime(date, '%x %X') or None
        return date


#
# Inspection Task (postit)
#


class InspectionTaskTitle(Mapper):
    """ """

    def mapTitle(self, line):
        return 'Transfert inspection bâti'


class InspectionTaskIdMapper(Mapper):
    """ """

    def mapId(self, line):
        return 'inspection-bati'


class InspectionTaskDateMapper(Mapper):
    """ """

    def mapDue_date(self, line):
        date = self.getData('dateIB')
        if not date:
            raise NoObjectToCreateException
        date = date and datetime.strptime(date, '%x %X') or None
        return date
