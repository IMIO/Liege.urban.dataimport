# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.mapper import AccessSimpleMapper as SimpleMapper

from Liege.urban.dataimport.buildlicence.mappers import LicenceFactory, \
    PortalTypeMapper, ReferenceMapper, WorkTypeMapper, CompletionStateMapper, \
    ErrorsMapper, CategoryMapper


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
                    'from': 'NUMERO DE DOSSIER',
                    'to': 'id',
                },
            ),

            PortalTypeMapper: {
                'from': (),
                'to': 'portal_type',
            },

#            CategoryMapper: {
#                'from': 'NORM_UNIK',
#                'to': 'foldercategory',
#            },

            ReferenceMapper: {
                'from': 'NUMERO DE DOSSIER',
                'to': 'reference',
            },

#            WorkTypeMapper: {
#                'from': 'Code_220+',
#                'to': 'workType',
#            },

#            CompletionStateMapper: {
#                'from': 'COLLDECISION',
#                'to': (),  # <- no field to fill, its the workflow state that has to be changed
#            },

            ErrorsMapper: {
                'from': (),
                'to': ('description',),  # log all the errors in the description field
            }
        },
    },
}
