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


class OldRubricFactory(BaseFactory):
    def getCreationPlace(self, factory_args):
        return self.site.portal_urban.rubrics.old_rubrics

# mappers

class PortalTypeMapper(Mapper):
    """ """

    def mapPortal_type(self, line):
        return 'EnvironmentRubricTerm'


class DescriptionMapper(Mapper):
    """ """

    def mapDescription(self, line):
        num = self.getData('num_rubrique2')
        desc = self.getData('libelle_rubrique2')
        full_desc = '{} - {}'.format(num, desc)
        return full_desc
