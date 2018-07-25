# -*- coding: utf-8 -*-

from zope.interface import implements

from Liege.urban.dataimport.interfaces import ILiegeEnvironmentOldRubricsImporter
from Liege.urban.dataimport.old_rubrics_env import objectsmapping
from imio.urban.dataimport.mapping import ObjectsMapping
from imio.urban.dataimport.mapping import ValuesMapping
from imio.urban.dataimport.Postgres.importer import PostgresDataImporter
from imio.urban.dataimport.Postgres.importer import PostgresImportSource


class EnvironmentOldRubricsImportSource(PostgresImportSource):
    """ """


class EnvironmentOldRubricsImporter(PostgresDataImporter):
    """ """

    implements(ILiegeEnvironmentOldRubricsImporter)

    def __init__(self, db_name='liege_environnement', table_name='tabrub2',
                 key_column='num_rubrique2', username='ro_user', password='',
                 host='devel.interne.imio.be', **kwargs):

        super(EnvironmentOldRubricsImporter, self).__init__(
            db_name,
            table_name,
            key_column,
            username,
            password,
            host,
            **kwargs
        )


class EnvironmentOldRubricsMapping(ObjectsMapping):
    """ """

    def getObjectsNesting(self):
        return objectsmapping.OBJECTS_NESTING

    def getFieldsMapping(self):
        return objectsmapping.FIELDS_MAPPINGS


class EnvironmentOldRubricsValuesMapping(ValuesMapping):
    """ """

    def getValueMapping(self, mapping_name):
        return None
