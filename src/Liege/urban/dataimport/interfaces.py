# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.theme.interfaces import IDefaultPloneLayer

from imio.urban.dataimport.interfaces import IUrbanDataImporter


class ILiegeUrbanDataimportLayer(IDefaultPloneLayer):
    """ Marker interface that defines a Zope 3 browser layer."""


class ILiegeBuildlicenceImporter(IUrbanDataImporter):
    """ Marker interface for ILiege buildlicence importer """


class ILiegeEnvironmentLicencesImporter(IUrbanDataImporter):
    """ Marker interface for ILiege buildlicence importer """


class ILiegeEnvironmentRubricsImporter(IUrbanDataImporter):
    """ Marker interface for ILiege rubrics importer """


class ILiegeEnvironmentOldRubricsImporter(IUrbanDataImporter):
    """ Marker interface for ILiege old rubrics importer """


class ILiegeMisclicenceImporter(IUrbanDataImporter):
    """ Marker interface for ILiege buildlicence importer """


class ILiegeArchivesImporter(IUrbanDataImporter):
    """ Marker interface for ILiege buildlicence importer """


class ILiegeArchitectsImporter(IUrbanDataImporter):
    """ Marker interface for ILiege architects importer """


class ILiegeInspectionImporter(IUrbanDataImporter):
    """ Marker interface for ILiege inspections importer """


class ILiegeInspectionMisclicenceImporter(IUrbanDataImporter):
    """ Marker interface for ILiege misclicence inspections importer """


class ILiegeTicketImporter(IUrbanDataImporter):
    """ Marker interface for ILiege tickets importer """
