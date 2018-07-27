# -*- coding: utf-8 -*-

from DateTime import DateTime

from imio.urban.dataimport.exceptions import NoObjectToCreateException
from imio.urban.dataimport.exceptions import NoFieldToMapException
from imio.urban.dataimport.factory import BaseFactory
from imio.urban.dataimport.Postgres.mapper import FieldMultiLinesSecondaryTableMapper
from imio.urban.dataimport.Postgres.mapper import SecondaryTableMapper
from imio.urban.dataimport.Postgres.mapper import PostgresFinalMapper as FinalMapper
from imio.urban.dataimport.Postgres.mapper import PostgresMapper as Mapper
from imio.urban.dataimport.Postgres.mapper import PostgresPostCreationMapper as PostCreationMapper

from plone import api

from Products.CMFPlone.utils import normalizeString
from Products.urban.interfaces import IEnvClassOne
from Products.urban.interfaces import IEnvClassThree
from Products.urban.interfaces import IEnvClassTwo
from Products.urban.interfaces import IUniqueLicence

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
        return self.getData('autoris').replace('/', '_')


class PortalTypeMapper(Mapper):
    """ """
    types_mapping = {
        '1': 'EnvClassOne',
        '2': 'EnvClassTwo',
        '3': 'EnvClassThree',
        'PU': 'UniqueLicence',
    }

    def mapPortal_type(self, line):
        ref = self.getData('autoris')
        nature = self.getData('nature')

        if nature == 'PU':
            return 'UniqueLicence'

        regex = '\d+/([1-3])/\d+'
        class_match = re.match(regex, ref)
        portal_type = None
        if class_match:
            class_num = class_match.groups()[0]
            portal_type = self.types_mapping.get(class_num, None)
            return portal_type

        regex = '\d+/.*N[1-5]'
        class_match = re.match(regex, ref)
        if class_match:
            portal_type = 'EnvClassTwo'
            return portal_type

        regex = '\d+/.*C3[4-8]'
        class_match = re.match(regex, ref)
        if class_match:
            portal_type = 'EnvClassOne'
            return portal_type

        if not portal_type:
            self.logError(self, line, 'No portal type found for this type value', {'TYPE value': ref})
            raise NoObjectToCreateException


class AuthorityMapper(Mapper):
    """ """

    def mapAuthority(self, line):
        deputation = self.getData('datdp')
        if deputation:
            return 'deputation-provinciale'
        raise NoFieldToMapException


class FolderManagerMapper(Mapper):
    """ """

    mapping = {
        '13': 'jean-francois-yernaux-technicien',
        '14': 'lucien-sanelli-technicien-1',
        '15': 'tony-lixon-technicien-1',
        '16': 'daniel-strykers-technicien-1',
    }

    def mapFoldermanagers(self, line):
        code = str(self.getData('codges'))
        foldermanager_id = self.mapping.get(code, None)
        if foldermanager_id is None:
            return None

        config = api.portal.get_tool('portal_urban')
        fm_folder = config.foldermanagers
        foldermanager = getattr(fm_folder, foldermanager_id)
        return [foldermanager]


class DescriptionMapper(Mapper):
    """ """

    def mapDescription(self, line):
        description = []

        ref_dp = self.getData('autorefdp')
        if ref_dp:
            description.append('<p>Référence dp: %s</p>' % ref_dp.encode('utf-8'))

        description = ''.join(description)
        return description


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
        raw_street_code = self.getData('nrue')
        if not raw_street_code:
            return []
        street_code = int(raw_street_code)
        street = self.streets_by_code.get(street_code, None)
        number = self.getData('numetab')[4:].encode('utf-8')
        if not street:
            self.logError(
                self,
                line,
                'Unknown street code', {
                    'street_code': street_code,
                    'street_name': self.getData('z_librue'),
                    'street_start': self.getData('z_ravpl'),
                    'street_number': number,
                }
            )
            return []
        return [{'street': street.UID(), 'number': number}]



class RubricsMapper(FieldMultiLinesSecondaryTableMapper):
    """ """
    def __init__(self, importer, args):
        super(RubricsMapper, self).__init__(importer, args)
        catalog = api.portal.get_tool('portal_catalog')

        rubrics_by_code = {}
        rubrics_brains = catalog(portal_type='EnvironmentRubricTerm',)
        rubrics = [br.getObject() for br in rubrics_brains]
        rubrics_by_code = dict([('old_rubrics' in r.getPhysicalPath() and r.id or r.id.replace('.', ''), r) for r in rubrics])
        self.rubrics_by_code = rubrics_by_code


    def mapRubrics(self, line):
        """ """
        self.line = line
        rubric_name = self.getData('classe').replace(' ', '')
        if rubric_name in self.rubrics_by_code:
            rubric = self.rubrics_by_code[rubric_name]
        else:
            import ipdb; ipdb.set_trace()

        return rubric


class CompletionStateMapper(PostCreationMapper):

    env_licence_mapping = {
        'final_decision_in_progress': [
            538, 548, 3100, 3516, 3519, 4270, 4280
        ],
        'refused': [
            425, 435, 445, 535, 545, 2950, 3090, 3400, 3517, 4260
        ],
        'abandoned': [
            437, 447, 537, 547
        ],
        'authorized': [
            None, 421, 422, 423, 424, 426, 431, 432, 433, 434, 436,
            441, 442, 443, 444, 446, 448,
            531, 532, 533, 534, 536,
            541, 542, 543, 544, 546,
            2910, 2920, 2930, 2940,
            3030, 3040, 3050, 3060, 3070,
            3300,
            3511, 3512, 3513, 3514, 3515,
            4410, 4420, 4430, 4440,
        ],
    }

    def map(self, line, plone_object):
        self.line = line
        workflow_tool = api.portal.get_tool('portal_workflow')
        raw_motif = self.getData('automotif')
        code = None
        if raw_motif:
            code = int(raw_motif)

        state = None
        if IEnvClassThree.providedBy(plone_object):
            if not code:
                state = 'acceptable'
            elif code in [6010, 6020, 6050, 6060]:
                state = 'acceptable'
            elif code in [6030]:
                state = 'inacceptable'
            elif code in [6040]:
                state = 'acceptable_with_conditions'

        elif IEnvClassTwo.providedBy(plone_object) or IEnvClassOne.providedBy(plone_object):
            if code in self.env_licence_mapping['final_decision_in_progress']:
                state = 'final_decision_in_progress'
            elif code in self.env_licence_mapping['refused']:
                state = 'refused'
            elif code in self.env_licence_mapping['abandoned']:
                state = 'abandoned'
            elif code in self.env_licence_mapping['authorized']:
                state = 'authorized'
            else:
                state = 'authorized'

        elif IUniqueLicence.providedBy(plone_object):
            if code in self.env_licence_mapping['final_decision_in_progress']:
                state = 'in_progress'
            elif code in self.env_licence_mapping['refused']:
                state = 'refused'
            elif code in self.env_licence_mapping['abandoned']:
                state = 'retired'
            elif code in self.env_licence_mapping['authorized']:
                state = 'accepted'
            else:
                state = 'accepted'

        if state:
            workflow_def = workflow_tool.getWorkflowsFor(plone_object)[0]
            workflow_id = workflow_def.getId()
            workflow_state = workflow_tool.getStatusOf(workflow_id, plone_object)
            workflow_state['review_state'] = state
            workflow_tool.setStatusOf(workflow_id, plone_object, workflow_state.copy())


class ErrorsMapper(FinalMapper):
    """ """

    def mapDescription(self, line, plone_object):

        line_number = self.importer.current_line
        errors = self.importer.errors.get(line_number, None)
        description = plone_object.Description()

        error_trace = []

        if errors:
            for error in errors:
                data = error.data
                if 'street' in error.message:
                    error = u'<p>adresse : %s, %s %s (%s) </p>' % (
                        data['street_number'], data['street_start'], data['street_name'], data['street_code']
                    )
                    error_trace.append(error.encode('utf-8'))
            error_trace.append('<br />')
        error_trace = ''.join(error_trace)

        return '%s%s' % (error_trace, description)


#
# PERSON/CORPORATION CONTACT
#

class CorporationFactory(BaseFactory):
    def getPortalType(self, container, **kwargs):
        return 'Corporation'

    def create(self, kwargs, container=None, line=None):
        review_state = kwargs.pop('state', None)
        corp = super(CorporationFactory, self).create(kwargs, container, line)
        if review_state:
            api.content.transition(obj=corp, to_state=review_state)
        return corp


class ContactIdMapper(Mapper):
    """ """

    def mapId(self, line):
        name = self.getData('firme')
        if not name:
            raise NoObjectToCreateException
        return normalizeString(name)


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


class OldCorporationStateMapper(Mapper):
     """
     Put old corporation on state 'disabled'
     """

     def mapState(self, line):
         return 'disabled'

#
# UrbanEvent base
#

# factory


class UrbanEventFactory(BaseFactory):
    """ """

    def create(self, kwargs, container, line):
        eventtype_uid = kwargs.pop('eventtype')
        title = kwargs.pop('title', None)
        if 'eventDate' not in kwargs:
            kwargs['eventDate'] = None
        urban_event = container.createUrbanEvent(eventtype_uid, **kwargs)
        if title:
            urban_event.setTitle(title)
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
# UrbanEvent final decision
#


class DecisionEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'decision_event'


class DecisionDateMapper(Mapper):

    def mapEventdate(self, line):
        date_decision_college = self.getData('datcol')
        date_decision_ft = self.getData('datdp')
        date = date_decision_ft or date_decision_college
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(str(date)) or None
        return date

    def mapDecisiondate(self, line):
        date_decision_college = self.getData('datcol')
        date_decision_ft = self.getData('datdp')
        date = date_decision_ft or date_decision_college
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(str(date)) or None
        return date

#
# UrbanEvent class 3 recevability event
#


class ClassThreeDecisionEventMapper(EventTypeMapper):
    """ """

    def mapEventtype(self, line):

        licence = self.importer.current_containers_stack[-1]
        urban_tool = api.portal.get_tool('portal_urban')
        config = urban_tool.getUrbanConfig(licence)

        eventtype_id = 'demande-recevable'
        raw_motif = self.getData('automotif')
        motif_code = None
        if raw_motif:
            motif_code = int(raw_motif)
        if motif_code in [6030]:
            eventtype_id = 'demande-irrecevable'

        return getattr(config.urbaneventtypes, eventtype_id).UID()

#
# UrbanEvent authorisation start
#


class AuthorisationStartEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'date-de-debut-de-lautorisation'


class AuthorisationStartDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('autodeb')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(str(date)) or None
        return date

#
# UrbanEvent authorisation end
#


class AuthorisationEndEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'date-de-fin-de-lautorisation'


class AuthorisationEndDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('autofin')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(str(date)) or None
        return date

#
# UrbanEvent forced authorisation end
#


class ForcedAuthorisationEndEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'fin-forcee-par-ladministration'


class ForcedAuthorisationEndDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('autofinfordate')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(str(date)) or None
        return date


class ForcedAuthorisationEndDescriptionMapper(Mapper):

    def mapMisc_description(self, line):
        raw_code = self.getData('automotif')
        code = None
        if raw_code:
            code = int(raw_code)
        code_mapping = self.getValueMapping('eventtitle_map')
        description = code_mapping.get(code, '')
        return description

#
# Misc UrbanEvent
#


class MiscEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'evenement-libre'


class MiscEventDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('datenvoi')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(str(date)) or None
        return date


class MiscEventTitle(Mapper):

    def mapTitle(self, line):
        code = self.getData('codenvoi')
        comment = self.getData('commentairenv')
        code_mapping = self.getValueMapping('eventtitle_map')
        title = code_mapping.get(code, '')
        if not title:
            title = comment
        return title

#
# Historic UrbanEvent
#


class HistoricEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'evenement-libre'


class HistoricEventDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('datretour')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(str(date)) or None
        return date


class HistoricEventTitle(Mapper):

    def mapTitle(self, line):
        code = self.getData('codretour')
        comment = self.getData('commentairet')
        code_mapping = self.getValueMapping('eventtitle_map')
        title = code_mapping.get(code, '')
        if not title:
            title = comment
        return title
