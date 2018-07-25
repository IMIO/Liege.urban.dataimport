# -*- coding: utf-8 -*-

from imio.urban.dataimport.Postgres.mapper import MultiLinesSecondaryTableMapper
from imio.urban.dataimport.Postgres.mapper import PostgresSimpleMapper as SimpleMapper
from imio.urban.dataimport.Postgres.mapper import SecondaryTableMapper

from Liege.urban.dataimport.environment import mappers


OBJECTS_NESTING = [
    ('LICENCE', [
        ('CORPORATION CONTACT', []),
        ('OLD CORPORATION CONTACT', []),
        ('MISC EVENT', []),
        ('HISTORIC EVENT', []),
        ('DECISION EVENT', []),
        ('AUTHORIZATION START EVENT', []),
        ('AUTHORIZATION END EVENT', []),
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

            mappers.AuthorityMapper: {
                'from': 'datdp',
                'to': 'authority',
            },

            mappers.DescriptionMapper: {
                'from': 'autorefdp',
                'to': 'description',
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
        'allowed_containers': ['EnvClassOne', 'EnvClassTwo'],

        'factory': [mappers.UrbanEventFactory],

        'mappers': {
            mappers.DecisionEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            mappers.DecisionDateMapper: {
                'from': ('datcol', 'datdp'),
                'to': ('eventDate', 'decisionDate'),
            },
        },
    },

    'CLASS 3 DECISION EVENT':
    {
        'allowed_containers': ['EnvClassThree'],

        'factory': [mappers.UrbanEventFactory],

        'mappers': {
            mappers.ClassThreeDecisionEventMapper: {
                'from': ('automotif'),
                'to': 'eventtype',
            },

            mappers.DecisionDateMapper: {
                'from': ('datcol', 'datdp'),
                'to': ('eventDate', 'decisionDate'),
            },
        },
    },

    'AUTHORIZATION START EVENT':
    {
        'factory': [mappers.UrbanEventFactory],

        'mappers': {
            mappers.AuthorisationStartEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            mappers.AuthorisationStartDateMapper: {
                'from': 'autodeb',
                'to': 'eventDate',
            },
        },
    },

    'AUTHORIZATION END EVENT':
    {
        'factory': [mappers.UrbanEventFactory],

        'mappers': {
            mappers.AuthorisationEndEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            mappers.AuthorisationEndDateMapper: {
                'from': 'autofin',
                'to': 'eventDate',
            },
        },
    },

    'FORCED AUTHORIZATION END EVENT':
    {
        'factory': [mappers.UrbanEventFactory],

        'mappers': {
            mappers.ForcedAuthorisationEndEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            mappers.ForcedAuthorisationEndDateMapper: {
                'from': 'autofinfordate',
                'to': 'eventDate',
            },

            mappers.ForcedAuthorisationEndDescriptionMapper: {
                'from': 'automotif',
                'to': 'misc_description',
            },
        },
    },

    'MISC EVENT':
    {
        'factory': [mappers.UrbanEventFactory],

        'mappers': {
            MultiLinesSecondaryTableMapper: {
                'table': 'tabenv',
                'KEYS': ('autoris', 'autoris'),
                'mappers': {
                    SimpleMapper: (
                        {
                            'from': 'commentairenv',
                            'to': 'misc_description',
                        },
                    ),

                    mappers.MiscEventMapper: {
                        'from': (),
                        'to': 'eventtype',
                    },

                    mappers.MiscEventDateMapper: {
                        'from': 'datenvoi',
                        'to': 'eventDate',
                    },

                    mappers.MiscEventTitle: {
                        'from': ('codenvoi', 'commentairenv'),
                        'to': 'title',
                    },

                },
            },
        },
    },

    'HISTORIC EVENT':
    {
        'factory': [mappers.UrbanEventFactory],

        'mappers': {
            MultiLinesSecondaryTableMapper: {
                'table': 'tabret',
                'KEYS': ('autoris', 'autoris'),
                'mappers': {
                    SimpleMapper: (
                        {
                            'from': 'commentairet',
                            'to': 'misc_description',
                        },
                    ),

                    mappers.HistoricEventMapper: {
                        'from': (),
                        'to': 'eventtype',
                    },

                    mappers.HistoricEventDateMapper: {
                        'from': 'datretour',
                        'to': 'eventDate',
                    },

                    mappers.HistoricEventTitle: {
                        'from': ('codretour', 'commentairet'),
                        'to': 'title',
                    },

                },
            },
        },
    },
}
