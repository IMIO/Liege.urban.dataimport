# -*- coding: utf-8 -*-

from zope.interface import implements

from Liege.urban.dataimport.interfaces import ILiegeEnvironmentLicencesImporter
from Liege.urban.dataimport.environment import objectsmapping
from Liege.urban.dataimport.environment import valuesmapping
from imio.urban.dataimport.mapping import ObjectsMapping
from imio.urban.dataimport.mapping import ValuesMapping
from imio.urban.dataimport.Postgres.importer import PostgresDataImporter
from imio.urban.dataimport.Postgres.importer import PostgresImportSource


class EnvironmentLicencesImportSource(PostgresImportSource):
    """ """


class EnvironmentLicencesImporter(PostgresDataImporter):
    """ """

    implements(ILiegeEnvironmentLicencesImporter)

    def __init__(self, db_name='liege_environnement', table_name='tabaut',
                 key_column='autoris', username='ro_user', password='',
                 host='devel.interne.imio.be', **kwargs):

        super(EnvironmentLicencesImporter, self).__init__(
            db_name,
            table_name,
            key_column,
            username,
            password,
            host,
            **kwargs
        )


class EnvironmentLicencesMapping(ObjectsMapping):
    """ """

    def getObjectsNesting(self):
        return objectsmapping.OBJECTS_NESTING

    def getFieldsMapping(self):
        return objectsmapping.FIELDS_MAPPINGS


class EnvironmentLicencesValuesMapping(ValuesMapping):
    """ """

    def getValueMapping(self, mapping_name):
        return valuesmapping.VALUES_MAPS.get(mapping_name, None)
