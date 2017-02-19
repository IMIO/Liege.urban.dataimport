# -*- coding: utf-8 -*-

from zope.interface import implements

from Liege.urban.dataimport.interfaces import ILiegeBuildlicenceImporter
from Liege.urban.dataimport.buildlicence import objectsmapping, valuesmapping

from imio.urban.dataimport.access.importer import AccessDataImporter as AccessImporter
from imio.urban.dataimport.mapping import ValuesMapping, ObjectsMapping


class BuildlicenceImporter(AccessImporter):
    """ """

    implements(ILiegeBuildlicenceImporter)

    def __init__(self, db_name='P_tables.mdb', table_name='PermisUrba_2017-2-17', key_column='NUMDOSSIERBKP', **kwargs):
        super(BuildlicenceImporter, self).__init__(db_name, table_name, key_column, **kwargs)


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
