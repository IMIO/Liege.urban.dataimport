# -*- coding: utf-8 -*-

from imio.urban.dataimport.Postgres.mapper import PostgresSimpleMapper as SimpleMapper

from Liege.urban.dataimport.environment import mappers


OBJECTS_NESTING = [
    ('LICENCE', [
        ('CORPORATION CONTACT', []),
    ],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [mappers.LicenceFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'signal',
                    'to': 'licenceSubject',
                },
                {
                    'from': 'numetab',
                    'to': 'reference',
                },
            ),

            mappers.IdMapper: {
                'from': 'numetab',
                'to': 'id',
            },

            mappers.PortalTypeMapper: {
                'from': 'clasprinc',
                'to': 'portal_type',
            },

            mappers.WorklocationsMapper: {
                'from': ('nrue', 'z_librue', 'z_ravpl',),
                'to': 'workLocations',
            },

            mappers.ErrorsMapper: {
                'from': (),
                'to': ('description',),  # log all the errors in the description field
            }
        },
    },

    'CORPORATION CONTACT':
    {
        'factory': [mappers.CorporationFactory],
        'mappers': {
            SimpleMapper: (
                {
                    'from': 'firme',
                    'to': 'denomination',
                },
                {
                    'from': 'resp',
                    'to': 'contactPersonName',
                },
                {
                    'from': 'exptel',
                    'to': 'contactPersonPhone',
                },
                {
                    'from': 'exppost',
                    'to': 'zipcode',
                },
                {
                    'from': 'exploc',
                    'to': 'city',
                },
            ),

            mappers.ContactIdMapper: {
                'from': 'firme',
                'to': 'id',
            },

            mappers.ContactStreetMapper: {
                'from': 'expadr',
                'to': ('street', 'number'),
            },
        },
    },
}
