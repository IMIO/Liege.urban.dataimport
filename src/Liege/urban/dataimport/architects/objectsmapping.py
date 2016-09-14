# -*- coding: utf-8 -*-

from Liege.urban.dataimport.architects.mappers import ArchitectFactory
from Liege.urban.dataimport.architects.mappers import NameMapper, \
    TitleMapper, StreetMapper, LocalityMapper

from imio.urban.dataimport.access.mapper import AccessSimpleMapper as SimpleMapper


OBJECTS_NESTING = [
    (
        'ARCHITECT', [
        ],
    ),
]

FIELDS_MAPPINGS = {
    'ARCHITECT':
    {
        'factory': [ArchitectFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'Numéro',
                    'to': 'id',
                },
                {
                    'from': 'Bureau',
                    'to': 'society',
                },
                {
                    'from': 'Tél',
                    'to': 'phone',
                },
                {
                    'from': 'Fax',
                    'to': 'fax',
                },
                {
                    'from': 'Matricule',
                    'to': 'registrationNumber',
                },
            ),

            TitleMapper: {
                'from': 'Titre',
                'to': 'personTitle',
            },

            NameMapper: {
                'from': 'Nom_Archi',
                'to': ('name1', 'name2'),
            },

            StreetMapper: {
                'from': 'Adresse',
                'to': ('street', 'number'),
            },

            LocalityMapper: {
                'from': 'CP Localité',
                'to': ('city', 'zipcode'),
            }
        },
    },
}
