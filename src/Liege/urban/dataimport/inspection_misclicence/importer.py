# -*- coding: utf-8 -*-

from zope.interface import implements

from Liege.urban.dataimport.interfaces import ILiegeInspectionMisclicenceImporter
from Liege.urban.dataimport.inspection_misclicence import objectsmapping, valuesmapping

from imio.urban.dataimport.csv.importer import CSVDataImporter as CSVImporter
from imio.urban.dataimport.mapping import ValuesMapping, ObjectsMapping


class InspectionMisclicenceImporter(CSVImporter):
    """ """

    implements(ILiegeInspectionMisclicenceImporter)

    delimiter = '#'
    quotechar = '"'
    escapechar = '\\'

    def __init__(self, csv_filename='T Aff Diverses', key_column='DOSSIER', **kwargs):
        super(InspectionMisclicenceImporter, self).__init__(csv_filename, key_column, **kwargs)


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
