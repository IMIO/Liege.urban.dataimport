# -*- coding: utf-8 -*-

from zope.interface import implements

from imio.urban.dataimport.access.importer import AccessDataImporter
from Liege.urban.dataimport.interfaces import ILiegeDataImporter


class LiegeDataImporter(AccessDataImporter):
    """ """

    implements(ILiegeDataImporter)
