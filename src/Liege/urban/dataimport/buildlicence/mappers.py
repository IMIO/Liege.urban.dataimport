# -*- coding: utf-8 -*-

from DateTime import DateTime

from imio.urban.dataimport.access.mapper import AccessFinalMapper as FinalMapper
from imio.urban.dataimport.access.mapper import AccessMapper as Mapper
from imio.urban.dataimport.access.mapper import AccessPostCreationMapper as PostCreationMapper

from imio.urban.dataimport.exceptions import NoObjectToCreateException

from imio.urban.dataimport.factory import BaseFactory

from plone import api

from Products.CMFPlone.utils import normalizeString

import re


#
# LICENCE
#

# factory


class LicenceFactory(BaseFactory):
    def getCreationPlace(self, factory_args):
        path = '%s/urban/buildlicences' % self.site.absolute_url_path()
        return self.site.restrictedTraverse(path)

# mappers


class ReferenceMapper(PostCreationMapper):
    def mapReference(self, line, plone_object):
        shore_abbr = {
            'right': u'D',
            'left': u'G',
            'center': u'C',
        }
        shore = shore_abbr.get(plone_object.shore, '')

        ref = 'PU/{} {}'.format(self.getData('NUMDOSSIERBKP'), shore)
        return ref


class TypeAndCategoryMapper(Mapper):
    """ """
    def mapPortal_type(self, line):
        type_value = self.getData('NORM_UNIK').upper()
        portal_type = self.getValueMapping('type_map')[type_value]['portal_type']
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


class ArchitectMapper(Mapper):
    """ """

    def mapArchitects(self, line):
        raw_archi_id = self.getData('NUMARCHITECTE')
        archi_id = raw_archi_id and str(int(float(raw_archi_id))) or ''
        archi = getattr(self.site.urban.architects, archi_id, None)
        return archi


class CompletionStateMapper(PostCreationMapper):
    def map(self, line, plone_object):
        self.line = line
        workflow_tool = api.portal.get_tool('portal_workflow')
        raw_state = self.getData('COLLDECISION').lower()
        if 'sans' in raw_state and 'suite' in raw_state:
            raw_state = 'sans suite'
        state_mapping = self.getValueMapping('state_map')
        state = state_mapping.get(raw_state, '')

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
# UrbanEvent base
#

# factory

class UrbanEventFactory(BaseFactory):
    """ """

    def getPortalType(self, **kwargs):
        return 'UrbanEvent'

    def create(self, kwargs, container, line):
        eventtype_uid = kwargs.pop('eventtype')
        urban_event = container.createUrbanEvent(eventtype_uid, **kwargs)
        return urban_event

#mappers


class EventTypeMapper(Mapper):
    """ """

    eventtype_id = ''  # to override

    def mapEventtype(self, line):
        licence = self.importer.current_containers_stack[-1]
        urban_tool = api.portal.get_tool('portal_urban')
        config = urban_tool.getUrbanConfig(licence)
        return getattr(config.urbaneventtypes, self.eventtype_id).UID()


#
# UrbanEvent deposit
#


class DepositEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'depot-de-la-demande'


class DepositDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('DEPOT')
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
