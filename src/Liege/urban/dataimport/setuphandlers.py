# -*- coding: utf-8 -*-


def isNotCurrentProfile(context):
    return context.readDataFile("liegeurbandataimport_marker.txt") is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context): return
    portal = context.getSite()
    addRubricValues(context)



def addRubricValues(context):
    site = context.getSite()
    config_folder = site.portal_urban.rubrics

    oldrubrics_folder_id = 'old_rubrics'
    if oldrubrics_folder_id in config_folder.objectIds():
        rubric_folder = getattr(config_folder, oldrubrics_folder_id)
    else:
        rubricfolder_id = config_folder.invokeFactory(
            "Folder",
            id=oldrubrics_folder_id,
            title="Rubrique reprise de données"
        )
        rubric_folder = getattr(config_folder, rubricfolder_id)
        rubric_folder.setConstrainTypesMode(1)
        rubric_folder.setLocallyAllowedTypes(['EnvironmentRubricTerm'])
        rubric_folder.setImmediatelyAddableTypes(['EnvironmentRubricTerm'])

