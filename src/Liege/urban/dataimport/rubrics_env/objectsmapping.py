# -*- coding: utf-8 -*-

from imio.urban.dataimport.Postgres.mapper import PostgresSimpleMapper as SimpleMapper

from Liege.urban.dataimport.rubrics_env import mappers


OBJECTS_NESTING = [
    ('LICENCE', [],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [mappers.RubricFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'libelle_rubrique1',
                    'to': 'description',
                },
            ),

            mappers.IdMapper: {
                'from': (
                    'classe_rubrique1',
                    'rubrique_rubrique1',
                    's_rubrique_rubrique1',
                    's_s_rubrique_rubrique1'
                ),
                'to': 'id',
            },

            mappers.PortalTypeMapper: {
                'from': (),
                'to': 'portal_type',
            },

            mappers.NumberMapper: {
                'from': (
                    'classe_rubrique1',
                    'rubrique_rubrique1',
                    's_rubrique_rubrique1',
                    's_s_rubrique_rubrique1'
                ),
                'to': 'number',
            },
        },
    },
}
