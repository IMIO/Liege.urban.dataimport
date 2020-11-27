# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.mapper import CSVSimpleMapper as SimpleMapper
from imio.urban.dataimport.factory import UrbanEventFactory

from Liege.urban.dataimport.ticket import mappers


OBJECTS_NESTING = [
    ('LICENCE', [
        ('ADDRESS POINT', []),
        ('TENANT', []),
        ('TENANT2', []),
        ('TENANT3', []),
        ('PROPRIETARY', []),
        ('TICKET SENT EVENT', []),
        ('TASKS', []),
    ],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [mappers.TicketFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'NUM_PARQUET',
                    'to': 'referenceProsecution',
                },
                {
                    'from': 'NUM_PV_POLICE',
                    'to': 'policeTicketReference',
                },
                {
                    'from': 'INFRACTION',
                    'to': 'licenceSubject',
                },
            ),

            mappers.IdMapper: {
                'from': 'NUMERO',
                'to': 'id',
            },

            mappers.ReferenceMapper: {
                'from': 'NUMERO',
                'to': 'reference',
            },

            mappers.OldAddressMapper: {
                'table': 'Rues_inspection',
                'KEYS': ('Correspondance_adr', 'Numero'),
                'mappers': {
                    mappers.WorklocationsMapper: {
                        'from': ('CODE_RUE', 'Localite', 'PARTICULE', 'RUE'),
                        'to': 'workLocations',
                    },
                }
            },

            mappers.OldAddressNumberMapper: {
                'from': ('NUM', 'Num2'),
                'to': 'workLocations',
            },

            mappers.BoundInspectionMapper: {
                'from': 'Mise en demeure',
                'to': 'bound_inspection',
            },

            mappers.BoundLicencesMapper: {
                'from': 'Dossiers',
                'to': 'bound_licences',
            },

            mappers.CompletionStateMapper: {
                'from': ('termine',),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },

            mappers.ErrorsMapper: {
                'from': (),
                'to': ('description',),  # log all the errors in the description field
            }
        },
    },

    'ADDRESS POINT':
    {
        'factory': [mappers.AddressFactory],

        'mappers': {
            mappers.AddressPointMapper: {
                'from': 'gidptadresse',
                'to': (),
            },

            mappers.TicketAddressPointTableMapper: {
                'table': 'PV_PlusieursPtadresses',
                'KEYS': ('NUMERO', 'numpv'),
                'mappers': {
                    mappers.AdditionalAddressPointMapper: {
                        'from': 'gid',
                        'to': (),
                    },
                }
            },
        },
    },

    'TENANT':
    {
        'factory': [mappers.ProprietaryFactory],
        'mappers': {
            SimpleMapper: (
                {
                    'from': 'A CHARGE DE',
                    'to': 'name1',
                },
            ),

            mappers.ProprietaryIdMapper: {
                'from': 'A CHARGE DE',
                'to': 'id',
            },

            mappers.ProprietaryAddressMapper: {
                'from': ('Adr1', 'Localite1'),
                'to': ('street', 'number', 'zipcode', 'city'),
            },
        },
    },

    'TENANT2':
    {
        'factory': [mappers.ProprietaryFactory],
        'mappers': {
            SimpleMapper: (
                {
                    'from': 'Charge 2',
                    'to': 'name1',
                },
            ),

            mappers.Proprietary2IdMapper: {
                'from': 'Charge 2',
                'to': 'id',
            },

            mappers.Proprietary2AddressMapper: {
                'from': ('Adr2', 'Localite2'),
                'to': ('street', 'number', 'zipcode', 'city'),
            },
        },
    },

    'TENANT3':
    {
        'factory': [mappers.ProprietaryFactory],
        'mappers': {
            SimpleMapper: (
                {
                    'from': 'Charge3',
                    'to': 'name1',
                },
            ),

            mappers.Proprietary3IdMapper: {
                'from': 'Charge3',
                'to': 'id',
            },

            mappers.Proprietary2AddressMapper: {
                'from': ('Adr3', 'Localite3'),
                'to': ('street', 'number', 'zipcode', 'city'),
            },
        },
    },

    'PROPRIETARY':
    {
        'factory': [mappers.ProprietaryFactory],
        'mappers': {
            SimpleMapper: (
                {
                    'from': 'PROPRIETAIRE',
                    'to': 'name1',
                },
            ),

            mappers.ContactIdMapper: {
                'from': 'PROPRIETAIRE',
                'to': 'id',
            },
        },
    },

    'TASKS':
    {
        'factory': [mappers.TaskFactory],

        'mappers': {
            mappers.TaskTableMapper: {
                'table': 'PV_Courriers',
                'KEYS': ('NUMERO', 'NUMERO'),
                'mappers': {
                    SimpleMapper: (
                        {
                            'from': 'Objet',
                            'to': 'title',
                        },
                    ),
                    mappers.TaskIdMapper: {
                        'from': 'numpiece',
                        'to': 'id',
                    },
                    mappers.TaskDescriptionMapper: {
                        'from': ('remarques', 'Destinataire', 'Expediteur', 'Expedition', 'Gestionnaire'),
                        'to': 'task_description',
                    },
                    mappers.TaskDateMapper: {
                        'from': 'Date',
                        'to': 'due_date',
                    }
                }
            }
        },
    },

    'TICKET SENT EVENT':
    {
        'factory': [UrbanEventFactory],

        'mappers': {
            mappers.TicketSentEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            mappers.TransmitDateMapper: {
                'from': 'TRANSMIS',
                'to': 'eventDate',
            },

            mappers.EventCompletionStateMapper: {
                'from': (),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },
        },
    },
}
