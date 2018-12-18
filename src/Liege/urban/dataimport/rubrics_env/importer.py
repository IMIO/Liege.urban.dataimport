# -*- coding: utf-8 -*-

from zope.interface import implements

from Liege.urban.dataimport.interfaces import ILiegeEnvironmentRubricsImporter
from Liege.urban.dataimport.rubrics_env import objectsmapping
from imio.urban.dataimport.mapping import ObjectsMapping
from imio.urban.dataimport.mapping import ValuesMapping
from imio.urban.dataimport.Postgres.importer import PostgresDataImporter
from imio.urban.dataimport.Postgres.importer import PostgresImportSource


class EnvironmentRubricsImportSource(PostgresImportSource):
    """ """


class EnvironmentRubricsImporter(PostgresDataImporter):
    """ """

    implements(ILiegeEnvironmentRubricsImporter)

    def __init__(self, db_name='liege_environnement', table_name='tabrub1',
                 key_column='classe_rubrique1', username='ro_user', password='',
                 host='devel.interne.imio.be', **kwargs):

        super(EnvironmentRubricsImporter, self).__init__(
            db_name,
            table_name,
            key_column,
            username,
            password,
            host,
            **kwargs
        )


class EnvironmentRubricsMapping(ObjectsMapping):
    """ """

    def getObjectsNesting(self):
        return objectsmapping.OBJECTS_NESTING

    def getFieldsMapping(self):
        return objectsmapping.FIELDS_MAPPINGS


class EnvironmentLicencesValuesMapping(ValuesMapping):
    """ """

    def getValueMapping(self, mapping_name):
        return None
