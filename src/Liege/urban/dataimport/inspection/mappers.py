# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.mapper import CSVFinalMapper as FinalMapper
from imio.urban.dataimport.csv.mapper import CSVMapper as Mapper
from imio.urban.dataimport.factory import BaseFactory


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
            error_trace.append('<br />')
        error_trace = ''.join(error_trace)

        return '%s%s' % (error_trace, description)
