# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.mapper import CSVSimpleMapper as SimpleMapper

from Liege.urban.dataimport.inspection import mappers


OBJECTS_NESTING = [
    ('LICENCE', [
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
                {
                    'from': 'N°',
                    'to': 'reference',
                },
            ),

            mappers.PortalTypeMapper: {
                'from': (),
                'to': 'portal_type',
            },

            mappers.ErrorsMapper: {
                'from': (),
                'to': ('description',),  # log all the errors in the description field
            }
        },
    },
}
