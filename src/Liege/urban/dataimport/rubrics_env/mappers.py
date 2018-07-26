# -*- coding: utf-8 -*-

from DateTime import DateTime

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


class RubricFactory(BaseFactory):
    def getCreationPlace(self, factory_args):
        return self.site.portal_urban.rubrics.old_rubrics

# mappers


class IdMapper(Mapper):
    """ """

    def mapId(self, line):
        rubric_id = self.getData('classe_rubrique1') + self.getData('rubrique_rubrique1')
        rubric_id = rubric_id + self.getData('s_rubrique_rubrique1') + self.getData('s_s_rubrique_rubrique1')
        return rubric_id


class NumberMapper(Mapper):
    """ """

    def mapNumber(self, line):
        rubric_id = self.getData('classe_rubrique1') + self.getData('rubrique_rubrique1')
        rubric_id = rubric_id + self.getData('s_rubrique_rubrique1') + self.getData('s_s_rubrique_rubrique1')
        return rubric_id


class PortalTypeMapper(Mapper):
    """ """

    def mapPortal_type(self, line):
        return 'EnvironmentRubricTerm'
