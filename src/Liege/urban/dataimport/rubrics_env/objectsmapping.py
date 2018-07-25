# -*- coding: utf-8 -*-

from Liege.urban.dataimport.rubrics_env import mappers


OBJECTS_NESTING = [
    ('LICENCE', [],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [mappers.RubricFactory],

        'mappers': {

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

            mappers.DescriptionMapper: {
                'from': (
                    'libelle_rubrique1',
                    'classe_rubrique1',
                    'rubrique_rubrique1',
                    's_rubrique_rubrique1',
                    's_s_rubrique_rubrique1'
                ),
                'to': 'description',
            },
        },
    },
}
