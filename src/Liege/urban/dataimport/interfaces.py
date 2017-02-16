# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.theme.interfaces import IDefaultPloneLayer

from imio.urban.dataimport.interfaces import IUrbanDataImporter


class ILiegeUrbanDataimportLayer(IDefaultPloneLayer):
    """ Marker interface that defines a Zope 3 browser layer."""


class ILiegeBuildlicenceImporter(IUrbanDataImporter):
    """ Marker interface for ILiege buildlicence importer """


class ILiegeMisclicenceImporter(IUrbanDataImporter):
    """ Marker interface for ILiege buildlicence importer """


class ILiegeArchivesImporter(IUrbanDataImporter):
    """ Marker interface for ILiege buildlicence importer """


class ILiegeArchitectsImporter(IUrbanDataImporter):
    """ Marker interface for ILiege architects importer """
