# -*- coding: utf-8 -*-

from zope.interface import implements

from Liege.urban.dataimport.interfaces import ILiegeBuildlicenceImporter
from Liege.urban.dataimport.buildlicence import objectsmapping, valuesmapping

from imio.urban.dataimport.csv.importer import CSVDataImporter as CSVImporter
from imio.urban.dataimport.mapping import ValuesMapping, ObjectsMapping


class BuildlicenceImporter(CSVImporter):
    """ """

    implements(ILiegeBuildlicenceImporter)

    delimiter = ';'

    def __init__(self, csv_filename='PermisUrba', key_column='NUMDOSSIERBKP', **kwargs):
        super(BuildlicenceImporter, self).__init__(csv_filename, key_column, **kwargs)


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
