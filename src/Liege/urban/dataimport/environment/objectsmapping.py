# -*- coding: utf-8 -*-

from imio.urban.dataimport.Postgres.mapper import MultiLinesSecondaryTableMapper
from imio.urban.dataimport.Postgres.mapper import PostgresSimpleMapper as SimpleMapper
from imio.urban.dataimport.Postgres.mapper import SecondaryTableMapper

from Liege.urban.dataimport.environment import mappers


OBJECTS_NESTING = [
    ('LICENCE', [
        ('CORPORATION CONTACT', []),
        ('OLD CORPORATION CONTACT', []),
        ('DECISION EVENT', []),
    ],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [mappers.LicenceFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'autoris',
                    'to': 'reference',
                },
            ),

            mappers.IdMapper: {
                'from': 'autoris',
                'to': 'id',
            },

            mappers.PortalTypeMapper: {
                'from': ('autoris', 'nature'),
                'to': 'portal_type',
            },

            SecondaryTableMapper: {
                'table': 'tabetab',
                'KEYS': ('numetab', 'numetab'),
                'mappers': {
                    SimpleMapper: (
                        {
                            'from': 'signal',
                            'to': 'licenceSubject',
                        },
                    ),
                    mappers.WorklocationsMapper: {
                        'from': ('numetab', 'nrue', 'z_librue', 'z_ravpl',),
                        'to': 'workLocations',
                    },
                },
            },

            mappers.RubricsMapper: {
                'table': 'tabrub',
                'KEYS': ('autoris', 'autoris'),
                'from': 'classe',
                'to': 'rubrics',
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
            SecondaryTableMapper: {
                'table': 'tabetab',
                'KEYS': ('numetab', 'numetab'),
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
        },
    },

    'OLD CORPORATION CONTACT':
    {
        'factory': [mappers.CorporationFactory],
        'mappers': {
            MultiLinesSecondaryTableMapper: {
                'table': 'tabexp',
                'KEYS': ('numetab', 'numetab'),
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

                    # disable each old corporation.
                    mappers.OldCorporationStateMapper: {
                        'from': (),
                        'to': 'state',
                    }
                },
            },
        },
    },

    'DECISION EVENT':
    {
        'factory': [mappers.UrbanEventFactory],

        'mappers': {
            mappers.DecisionEventMapper: {
                'from': ('datcol', 'datdp'),
                'to': 'eventtype',
            },

            mappers.DecisionDateMapper: {
                'from': ('datcol', 'datdp'),
                'to': ('eventDate', 'decisionDate'),
            },
        },
    },
}
