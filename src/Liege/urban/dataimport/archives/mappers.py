# -*- coding: utf-8 -*-

from DateTime import DateTime

from imio.urban.dataimport.access.mapper import AccessFinalMapper as FinalMapper
from imio.urban.dataimport.access.mapper import AccessMapper as Mapper
from imio.urban.dataimport.access.mapper import AccessPostCreationMapper as PostCreationMapper
from imio.urban.dataimport.access.mapper import SecondaryTableMapper
from imio.urban.dataimport.config import IMPORT_FOLDER_PATH
from imio.urban.dataimport.exceptions import NoFieldToMapException
from imio.urban.dataimport.exceptions import NoObjectToCreateException
from imio.urban.dataimport.factory import BaseFactory
from imio.urban.dataimport.utils import parse_date

from plone import api

from Products.CMFPlone.utils import normalizeString

#
# LICENCE
#

# factory


class LicenceFactory(BaseFactory):

    def getPortalType(self, container=None, **kwargs):
        return 'BuildLicence'

    def getCreationPlace(self, factory_args):
        path = '{}/urban/buildlicences'.format(self.site.absolute_url_path())
        return self.site.restrictedTraverse(path)

# mappers


class LicenceSubjectMapper(SecondaryTableMapper):
    """ """


class StreetTableMapper(SecondaryTableMapper):
    """ """

    def get_db_path(self):
        return '{}/TablesDesRues2003.mdb'.format(IMPORT_FOLDER_PATH)


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

    def mapWorklocations(self, line):
        """ """
        raw_street_code = line[1]
        if not raw_street_code:
            return []
        street_code = int(raw_street_code)
        street = self.streets_by_code.get(street_code, None)
        if not street:
            return []
        return [{'street': street.UID(), 'number': ''}]


class OldLocationMapper(Mapper):
    """ """

    def mapDescription(self, line):
        description_lines = []

        rep1 = self.getData('Repère1')
        rep1b = self.getData('Repère1b')
        rep3 = self.getData('Repère3')
        if rep1 == rep1b:
            location = self.getValueMapping('repere_map').get(rep1, rep1)
            description_lines.append('<p>localité: {}</p>'.format(location))
        else:
            rep_line = '<p>repères: {}, {}, {}</p>'.format(rep1, rep1b, rep3)
            description_lines.append(rep_line)

        old_street_name = self.getData('AncienNomRue')
        if old_street_name:
            description_lines.append('<p>ancien nom de rue: {}</p>'.format(old_street_name))

        return ''.join(description_lines) + '<br/>'


class StreetNumberMapper(PostCreationMapper):
    """ """

    def map(self, line, plone_object):
        self.line = line
        licence = plone_object
        address = licence.getWorkLocations()
        if address:
            address[0]['number'] = self.getData('NumPol')
            licence.setWorkLocations(address)
        else:
            street = '%s %s' % (self.getData('Particule'), self.getData('Rue'))
            num = self.getData('NumPol')
            self.logError(self, line, 'street not found', {'address': street, 'num': num})


class CompletionStateMapper(PostCreationMapper):
    def map(self, line, plone_object):
        self.line = line
        workflow_tool = api.portal.get_tool('portal_workflow')

        workflow_def = workflow_tool.getWorkflowsFor(plone_object)[0]
        workflow_id = workflow_def.getId()
        workflow_state = workflow_tool.getStatusOf(workflow_id, plone_object)
        workflow_state['review_state'] = 'accepted'
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
                if 'street' in error.message:
                    error_trace.append('<p>adresse : %s %s </p>' % (data['num'], data['address']))
                if 'decision date' in error.message:
                    error_trace.append('<p>date de la decision : %s </p>' % data['date'])
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

# mappers


class ContactIdMapper(Mapper):
    """ """

    def mapId(self, line):
        name = self.getData('Propriétaire')
        if not name:
            raise NoObjectToCreateException

        return normalizeString(self.site.portal_urban.generateUniqueId(name))
#
# UrbanEvent base
#

# factory

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

        return getattr(config.urbaneventtypes, self.eventtype_id).UID()


#
# UrbanEvent college final decision
#


class DecisionEventMapper(EventTypeMapper):
    """ """
    eventtype_id = 'delivrance-du-permis-octroi-ou-refus'


class DecisionDateMapper(PostCreationMapper):

    def mapEventdate(self, line, plone_object):
        date = self.getData('Date')
        try:
            date = date and parse_date(date) or None
        except:
            self.logError(self, line, 'decision date wrong format', {'date': date})
            raise NoFieldToMapException
        if not date:
            raise NoFieldToMapException
        if int(date.year) > 2017:
            new_date = '%s/%s/%s' % (str(int(date.year) - 100), date.month, date.day)
            date = DateTime(new_date)
        return date


class EventCompletionStateMapper(PostCreationMapper):
    def map(self, line, plone_object):
        self.line = line
        workflow_tool = api.portal.get_tool('portal_workflow')

        workflow_def = workflow_tool.getWorkflowsFor(plone_object)[0]
        workflow_id = workflow_def.getId()
        workflow_state = workflow_tool.getStatusOf(workflow_id, plone_object)
        workflow_state['review_state'] = 'closed'
        workflow_tool.setStatusOf(workflow_id, plone_object, workflow_state.copy())
