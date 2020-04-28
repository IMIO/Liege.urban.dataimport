# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.mapper import CSVSimpleMapper as SimpleMapper

from Liege.urban.dataimport.inspection import mappers


OBJECTS_NESTING = [
    ('LICENCE', [
        ('PROPRIETARY', []),
    ],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [mappers.InspectionFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'N°',
                    'to': 'id',
                },
            ),

            mappers.PortalTypeMapper: {
                'from': (),
                'to': 'portal_type',
            },

            mappers.ReferenceMapper: {
                'from': 'numerorapport',
                'to': 'reference',
            },

            mappers.OldAddressMapper: {
                'table': 'Rues',
                'KEYS': ('ref_rue', 'Numero'),
                'mappers': {
                    mappers.WorklocationsMapper: {
                        'from': ('CODE_RUE', 'Localite', 'PARTICULE', 'RUE'),
                        'to': 'workLocations',
                    },
                }
            },

            mappers.OldAddressNumberMapper: {
                'from': ('NUM', 'Num2'),
                'to': 'workLocations',
            },

            mappers.ErrorsMapper: {
                'from': (),
                'to': ('description',),  # log all the errors in the description field
            }
        },
    },

    'PROPRIETARY':
    {
        'factory': [mappers.ProprietaryFactory],
        'mappers': {
            SimpleMapper: (
                {
                    'from': 'proprio',
                    'to': 'name1',
                },
            ),

            mappers.ContactIdMapper: {
                'from': 'proprio',
                'to': 'id',
            },
        },
    },
}
