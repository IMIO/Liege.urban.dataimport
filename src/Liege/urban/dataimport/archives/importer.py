# -*- coding: utf-8 -*-

from zope.interface import implements

from Liege.urban.dataimport.interfaces import ILiegeArchivesImporter
from Liege.urban.dataimport.archives import objectsmapping

from imio.urban.dataimport.access.importer import AccessDataImporter as AccessImporter
from imio.urban.dataimport.mapping import ObjectsMapping, ValuesMapping


class ArchivesImporter(AccessImporter):
    """ """

    implements(ILiegeArchivesImporter)

    def __init__(self, db_name='Archives2013.mdb', table_name='Après 1977', key_column='Dossier', **kwargs):
        super(ArchivesImporter, self).__init__(db_name, table_name, key_column, **kwargs)


class LiegeArchivesMapping(ObjectsMapping):
    """ """

    def getObjectsNesting(self):
        return objectsmapping.OBJECTS_NESTING

    def getFieldsMapping(self):
        return objectsmapping.FIELDS_MAPPINGS


class ArchivesValuesMapping(ValuesMapping):
    """ """

    def getValueMapping(self, mapping_name):
        return {}