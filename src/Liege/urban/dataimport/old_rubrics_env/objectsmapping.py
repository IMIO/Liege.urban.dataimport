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
                {
                    'from': 'num_rubrique2',
                    'to': 'number',
                },
                {
                    'from': 'libelle_rubrique2',
                    'to': 'description',
                },
            ),

            mappers.PortalTypeMapper: {
                'from': (),
                'to': 'portal_type',
            },

            mappers.ClassMapper: {
                'from': 'classe_rubrique2',
                'to': 'extraValue',
            },
        },
    },
}
