# -*- coding: utf-8 -*-

from DateTime import DateTime

from imio.urban.dataimport.csv.mapper import CSVFinalMapper as FinalMapper
from imio.urban.dataimport.csv.mapper import CSVMapper as Mapper
from imio.urban.dataimport.csv.mapper import CSVPostCreationMapper as PostCreationMapper
from imio.urban.dataimport.csv.mapper import SecondaryTableMapper
from imio.urban.dataimport.exceptions import NoFieldToMapException
from imio.urban.dataimport.exceptions import NoObjectToCreateException
from imio.urban.dataimport.factory import BaseFactory
from imio.urban.dataimport.utils import parse_date

from plone import api

from Products.CMFPlone.utils import normalizeString

from unidecode import unidecode


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
        return self.getData('numerorapport')


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
        return getattr(config.urbaneventtypes, self.eventtype_id).UID()


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
