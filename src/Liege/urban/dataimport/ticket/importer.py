# -*- coding: utf-8 -*-

from zope.interface import implements

from Liege.urban.dataimport.interfaces import ILiegeTicketImporter
from Liege.urban.dataimport.ticket import objectsmapping, valuesmapping

from imio.urban.dataimport.csv.importer import CSVDataImporter as CSVImporter
from imio.urban.dataimport.mapping import ValuesMapping, ObjectsMapping


class TicketImporter(CSVImporter):
    """ """

    implements(ILiegeTicketImporter)

    delimiter = '#'
    quotechar = '"'
    escapechar = '\\'

    def __init__(self, csv_filename='PVerbaux_data', key_column='NUMERO', **kwargs):
        super(TicketImporter, self).__init__(csv_filename, key_column, **kwargs)


class LiegeMapping(ObjectsMapping):
    """ """

    def getObjectsNesting(self):
        return objectsmapping.OBJECTS_NESTING

    def getFieldsMapping(self):
        return objectsmapping.FIELDS_MAPPINGS


class LicencesValuesMapping(ValuesMapping):
    """ """

    def getValueMapping(self, mapping_name):
        return valuesmapping.VALUES_MAPS.get(mapping_name, None)
