# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.mapper import AccessSimpleMapper as SimpleMapper

from Liege.urban.dataimport.buildlicence.mappers import LicenceFactory, \
    TypeAndCategoryMapper, ReferenceMapper, CompletionStateMapper, ErrorsMapper, \
    FolderCategoryMapper


OBJECTS_NESTING = [
    (
        'LICENCE', [
        ],
    ),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [LicenceFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'NUMDOSSIERBKP',
                    'to': 'id',
                },
                {
                    'from': 'Objettrav',
                    'to': 'licenceSubject',
                },
            ),

            TypeAndCategoryMapper: {
                'from': 'NORM_UNIK',
                'to': ('portal_type', 'foldercategory'),
            },

            FolderCategoryMapper: {
                'from': 'CODE NAT TRAVAUX',
                'to': 'folderCategoryTownship',
            },

            ReferenceMapper: {
                'from': 'NUMDOSSIERBKP',
                'to': 'reference',
            },

            CompletionStateMapper: {
                'from': 'COLLDECISION',
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },

            ErrorsMapper: {
                'from': (),
                'to': ('description',),  # log all the errors in the description field
            }
        },
    },
}
