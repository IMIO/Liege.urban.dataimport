# -*- coding: utf-8 -*-

from imio.urban.dataimport.Postgres.mapper import PostgresSimpleMapper as SimpleMapper

from Liege.urban.dataimport.old_rubrics_env import mappers


OBJECTS_NESTING = [
    ('LICENCE', [],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [mappers.OldRubricFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'num_rubrique2',
                    'to': 'id',
                },
            ),

            mappers.PortalTypeMapper: {
                'from': (),
                'to': 'portal_type',
            },

            mappers.DescriptionMapper: {
                'from': ('libelle_rubrique2', 'num_rubrique2'),
                'to': 'description',
            },
        },
    },
}
