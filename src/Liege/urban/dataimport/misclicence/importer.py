# -*- coding: utf-8 -*-

from zope.interface import implements

from Liege.urban.dataimport.interfaces import ILiegeMisclicenceImporter
from Liege.urban.dataimport.misclicence import objectsmapping, valuesmapping

from imio.urban.dataimport.access.importer import AccessDataImporter as AccessImporter
from imio.urban.dataimport.mapping import ValuesMapping, ObjectsMapping


class MisclicenceImporter(AccessImporter):
    """ """

    implements(ILiegeMisclicenceImporter)

    def __init__(self, db_name='P_tables.mdb', table_name='T Aff Diverses', key_column='DOSSIER', **kwargs):
        super(MisclicenceImporter, self).__init__(db_name, table_name, key_column, **kwargs)


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
