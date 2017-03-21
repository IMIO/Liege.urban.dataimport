# -*- coding: utf-8 -*-

from zope.interface import implements

from Liege.urban.dataimport.interfaces import ILiegeArchitectsImporter
from Liege.urban.dataimport.architects import objectsmapping, valuesmapping

from imio.urban.dataimport.access.importer import AccessDataImporter as AccessImporter
from imio.urban.dataimport.mapping import ValuesMapping, ObjectsMapping


class ArchitectsImporter(AccessImporter):
    """ """

    implements(ILiegeArchitectsImporter)

    def __init__(self, db_name='P_tables.mdb', table_name='T Architecte', key_column='Numéro', **kwargs):
        super(ArchitectsImporter, self).__init__(db_name, table_name, key_column, **kwargs)


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
