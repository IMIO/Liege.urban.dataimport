# -*- coding: utf-8 -*-

from imio.urban.dataimport.factory import UrbanEventFactory
from imio.urban.dataimport.Postgres.mapper import MultiLinesSecondaryTableMapper
from imio.urban.dataimport.Postgres.mapper import PostgresSimpleMapper as SimpleMapper
from imio.urban.dataimport.Postgres.mapper import SecondaryTableMapper

from Liege.urban.dataimport.environment import mappers


OBJECTS_NESTING = [
    ('LICENCE', [
        ('CORPORATION CONTACT', []),
        ('OLD CORPORATION CONTACT', []),
        ('OWNER CHANGE EVENT', []),
        ('MISC EVENT', []),
        ('HISTORIC EVENT', []),
        ('DECISION EVENT', []),
        ('CLASS 3 DECISION EVENT', []),
        ('AUTHORIZATION START EVENT', []),
        ('AUTHORIZATION END EVENT', []),
        ('FORCED AUTHORIZATION END EVENT', []),
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
                {
                    'from': 'autorefrw',
                    'to': 'referenceDGATLP',
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

            mappers.referenceForUniqueLicence: {
                'from': 'autoris',
                'to': 'referenceSPE',
            },

            mappers.AuthorityMapper: {
                'from': ('datdp', 'datrw', 'automotif'),
                'to': 'authority',
            },

            mappers.DescriptionMapper: {
                'from': ('autorefdp', 'automotif', 'automotif'),
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

                    mappers.FolderManagerMapper: {
                        'from': 'codges',
                        'to': 'foldermanagers',
                    },

                    mappers.WorklocationsMapper: {
                        'from': ('numetab', 'nrue', 'z_librue', 'z_ravpl', 'autoris'),
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

            mappers.CompletionStateMapper: {
                'table': 'tabenv',
                'KEYS': ('autoris', 'autoris'),
                'from': ('codenvoi', 'datcol', 'datdp', 'datrw'),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
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

    'OWNER CHANGE EVENT':
    {
        'factory': [UrbanEventFactory],
        'mappers': {
            MultiLinesSecondaryTableMapper: {
                'table': 'tabexp',
                'KEYS': ('numetab', 'numetab'),
                'mappers': {
                    mappers.OwnerChangeEventMapper: {
                        'from': (),
                        'to': 'eventtype',
                    },

                    mappers.OwnerChangeEventTitle: {
                        'from': 'firme',
                        'to': 'title',
                    },

                    mappers.OwnerChangeEventDate: {
                        'from': 'expfin',
                        'to': 'eventDate',
                    },
                },
            },
        },
    },

    'DECISION EVENT':
    {
        'allowed_containers': [
            'EnvClassOne',
            'EnvClassTwo',
            'UniqueLicence',
            'EnvClassBordering'
        ],

        'factory': [UrbanEventFactory],

        'mappers': {
            mappers.DecisionEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            mappers.DecisionDateMapper: {
                'from': ('datcol', 'datdp', 'datrw'),
                'to': ('eventDate', 'decisionDate'),
            },
        },
    },

    'CLASS 3 DECISION EVENT':
    {
        'allowed_containers': ['EnvClassThree'],

        'factory': [UrbanEventFactory],

        'mappers': {
            mappers.ClassThreeDecisionEventMapper: {
                'from': ('automotif'),
                'to': 'eventtype',
            },

            mappers.DecisionDateMapper: {
                'from': ('datcol', 'datdp', 'datrw'),
                'to': ('eventDate', 'decisionDate'),
            },
        },
    },

    'AUTHORIZATION START EVENT':
    {
        'factory': [UrbanEventFactory],

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
        'factory': [UrbanEventFactory],

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
        'factory': [UrbanEventFactory],

        'allowed_containers': ['EnvClassOne', 'EnvClassTwo', 'EnvClassThree'],

        'mappers': {
            mappers.ForcedAuthorisationEndEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            mappers.ForcedAuthorisationEndDateMapper: {
                'from': 'autofinfor',
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
        'factory': [UrbanEventFactory],

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
                        'from': ('codenvoi'),
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
        'factory': [UrbanEventFactory],

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
