# -*- coding: utf-8 -*-

from DateTime import DateTime

from imio.urban.dataimport.csv.mapper import CSVFinalMapper as FinalMapper
from imio.urban.dataimport.csv.mapper import CSVMapper as Mapper
from imio.urban.dataimport.csv.mapper import CSVPostCreationMapper as PostCreationMapper
from imio.urban.dataimport.csv.mapper import MultiLinesSecondaryTableMapper
from imio.urban.dataimport.csv.mapper import SecondaryTableMapper
from imio.urban.dataimport.exceptions import NoFieldToMapException
from imio.urban.dataimport.exceptions import NoObjectToCreateException
from imio.urban.dataimport.factory import BaseFactory
from imio.urban.dataimport.utils import parse_date

from liege.urban.services import address_service

from plone import api

from Products.CMFPlone.utils import normalizeString

from unidecode import unidecode

import re


#
# Inspection
#

# factory

class InspectionFactory(BaseFactory):
    def getCreationPlace(self, factory_args):
        path = '{}/urban/inspections'.format(self.site.absolute_url_path())
        return self.site.restrictedTraverse(path)

# mappers


class PortalTypeMapper(Mapper):
    """ """

    def mapPortal_type(self, line):
        return 'Inspection'


class ReferenceMapper(PostCreationMapper):
    """ """

    def mapReference(self, line, plone_object):
        abbr = 'IB'
        ref = '{}/{}'.format(abbr, str(int(float(self.getData('numerorapport').replace(',', '.') or '0.0'))))
        return ref


class FoldermanagersMapper(PostCreationMapper):
    """ """

    def mapFoldermanagers(self, line, plone_object):

        inspectors_mapping = self.getValueMapping('inspectors')
        portal_urban = self.site.portal_urban
        foldermanagers = portal_urban.foldermanagers

        foldermanager_id = inspectors_mapping.get(self.getData('ref_inspecteur'), None)
        if not foldermanager_id:
            raise NoFieldToMapException

        foldermanager = getattr(foldermanagers, foldermanager_id, None)
        if not foldermanager:
            self.logError(self, line, 'inspector', {'name': foldermanager_id})
            raise NoFieldToMapException

        # plone_object.setFoldermanagers(foldermanager.UID())
        return foldermanager.UID()


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


class ComplaintTableMapper(SecondaryTableMapper):
    """ """


class ComplaintTextMapper(Mapper):

    def mapInspectiondescription(self, line):
        plainte = '<p>{}</p>'.format(self.getData('plainte'))
        plainte = plainte.replace('\n', '<br/>').replace('\r', '<br/>')
        return plainte


class InfosTableMapper(SecondaryTableMapper):
    """ """


class InfosTextMapper(Mapper):

    def mapDescription(self, line):
        infos = '<p>{}</p>'.format(self.getData('infos'))
        infos = infos.replace('\n', '<br/>').replace('\r', '<br/>')
        return infos


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
        kwargs['id'] = normalizeString(self.site.portal_urban.generateUniqueId(kwargs['capakey']))
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
        session.close()
        if address_record:
            return address_record._asdict()


class InspectionAddressPointTableMapper(MultiLinesSecondaryTableMapper):
    """ """


class AdditionalAddressPointMapper(Mapper):

    def map(self, line):
        """
        """
        gid = self.getData('gidnum', line)
        session = address_service.new_session()
        address_record = session.query_address_by_gid(gid)
        session.close()
        if address_record:
            return address_record._asdict()
        return {}


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

    def mapId(self, line):
        name = self.getData('proprio')
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

#
# UrbanEvent base
#

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
        return getattr(config.urbaneventtypes, self.eventtype_id).UID()


class ReportTableMapper(SecondaryTableMapper):
    """ """


class ReportEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'rapport'


class InspectDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('date_constat')
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(parse_date(date)) or None
        return date


class ReportDateMapper(Mapper):

    def mapReportdate(self, line):
        date = self.getData('date_rapport')
        date = date and DateTime(parse_date(date)) or None
        return date


class ReportTextMapper(Mapper):

    def mapReport(self, line):
        report = '<p>{}</p>'.format(self.getData('rapport'))
        report = report.replace('\n', '<br/>').replace('\r', '<br/>')
        return report


class EventCompletionStateMapper(PostCreationMapper):
    def map(self, line, plone_object):
        self.line = line
        workflow_tool = api.portal.get_tool('portal_workflow')

        workflow_def = workflow_tool.getWorkflowsFor(plone_object)[0]
        workflow_id = workflow_def.getId()
        workflow_state = workflow_tool.getStatusOf(workflow_id, plone_object)
        workflow_state['review_state'] = 'closed'
        workflow_tool.setStatusOf(workflow_id, plone_object, workflow_state.copy())


class ArticlesTableMapper(SecondaryTableMapper):
    """ """


class ArticleTextMapper(Mapper):

    def mapOffense_articles_details(self, line):
        article = '<p>{}</p>'.format(self.getData('ref_cwatup'))
        article = article.replace('\n', '<br/>').replace('\r', '<br/>')
        return article


class FollowupEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'followup-access'


class FollowupsMapper(MultiLinesSecondaryTableMapper):
    """ """


class FollowupDateMapper(Mapper):

    def mapEventdate(self, line):
        date = self.getData('date_encodage', line)
        if not date:
            raise NoObjectToCreateException
        date = date and DateTime(parse_date(date)) or None
        return date


class FollowupMapper(Mapper):
    """ """

    def mapMisc_description(self, line):
        piece = self.getData('piece', line)
        writer = self.getData('encodeur', line)
        comment = self.getData('suite', line)
        if not comment:
            raise NoObjectToCreateException
        text = '<p>Pièce: {}</p><p>Encodeur: {}</p><P>Suite: {}</p>'.format(
            piece,
            writer,
            comment
        )
        return text


class CommentEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'commentaire-reprise-access'


class CommentsMapper(SecondaryTableMapper):
    """ """


class CommentMapper(Mapper):
    """ """

    def mapMisc_description(self, line):
        comment = self.getData('commentaires', line)
        if not comment:
            raise NoObjectToCreateException
        return '<p>{}</p>'.format(comment)
