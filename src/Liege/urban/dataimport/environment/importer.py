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

    def iterdata(self):

        result = self.session.query(self.main_table)
        wrkdossier = self.importer.datasource.get_table('tabetab')

        # default:
        records = result.order_by(wrkdossier.columns['numetab'].desc()).all()
        return records


class EnvironmentLicencesImporter(PostgresDataImporter):
    """ """

    implements(ILiegeEnvironmentLicencesImporter)

    def __init__(self, db_name='liege_environnement', table_name='tabetab', key_column='numetab', **kwargs):
        super(EnvironmentLicencesImporter, self).__init__(db_name, table_name, key_column, **kwargs)


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
