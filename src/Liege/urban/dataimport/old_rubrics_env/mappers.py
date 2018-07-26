# -*- coding: utf-8 -*-

from DateTime import DateTime

from imio.urban.dataimport.exceptions import NoFieldToMapException
from imio.urban.dataimport.exceptions import NoObjectToCreateException
from imio.urban.dataimport.factory import BaseFactory
from imio.urban.dataimport.Postgres.mapper import SecondaryTableMapper
from imio.urban.dataimport.Postgres.mapper import PostgresFinalMapper as FinalMapper
from imio.urban.dataimport.Postgres.mapper import PostgresMapper as Mapper

from plone import api

from Products.CMFPlone.utils import normalizeString

from unidecode import unidecode

import re


#
# Rubrics terms
#

# factory


class OldRubricFactory(BaseFactory):
    def getCreationPlace(self, factory_args):
        return self.site.portal_urban.rubrics.old_rubrics

# mappers

class PortalTypeMapper(Mapper):
    """ """

    def mapPortal_type(self, line):
        return 'EnvironmentRubricTerm'


class ClassMapper(Mapper):
    """ """

    def mapExtravalue(self, line):
        classe = str(self.getData('classe_rubrique2'))
        if classe == '6':
            raise NoFieldToMapException
        return classe
