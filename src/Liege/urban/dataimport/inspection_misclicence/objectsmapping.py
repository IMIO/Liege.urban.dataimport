# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.mapper import CSVSimpleMapper as SimpleMapper

from Liege.urban.dataimport.inspection_misclicence import mappers


OBJECTS_NESTING = [
    ('LICENCE', [
        ('PERSON CONTACT', []),
        ('ADDRESS POINT', []),
        ('DEPOSIT EVENT', []),
        ('TASKS', []),
    ],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [mappers.LicenceFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'Objettrav',
                    'to': 'licenceSubject',
                },
            ),

            mappers.IdMapper: {
                'from': 'DOSSIER',
                'to': 'id',
            },

            mappers.PortalTypeMapper: {
                'from': ('Type_trav', 'Objettrav', 'COLLEGE_DECISION'),
                'to': 'portal_type',
            },

            mappers.ReferenceMapper: {
                'from': ('DOSSIER', 'Type_trav', 'COLLEGE_DECISION'),
                'to': 'reference',
            },

            mappers.OldAddressMapper: {
                'table': 'Rues_inspection',
                'KEYS': ('Correspondance_rue', 'Numero'),
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

            mappers.CompletionStateMapper: {
                'from': 'COLLEGE_DECISION',
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },

            mappers.ErrorsMapper: {
                'from': (),
                'to': ('description',),  # log all the errors in the description field
            }
        },
    },

    'PERSON CONTACT':
    {
        'factory': [mappers.ContactFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'TELDEMANDEUR',
                    'to': 'phone',
                },
                {
                    'from': 'NOM DU DEMANDEUR',
                    'to': 'name1',
                },
            ),

            mappers.ContactIdMapper: {
                'from': ('QUALITE', 'NOM DU DEMANDEUR'),
                'to': 'id',
            },

            mappers.ContactStreetMapper: {
                'from': 'ADRESSE DEMANDEUR',
                'to': ('street', 'number'),
            },

            mappers.LocalityMapper: {
                'from': ('CODE POSTAL22', 'LOCALITE22'),
                'to': ('city', 'zipcode'),
            }
        },
    },

    'ADDRESS POINT':
    {
        'factory': [mappers.AddressFactory],

        'mappers': {
            mappers.AddressPointMapper: {
                'from': ('gidptadresse', 'capakey', 'Numero', 'Correspondance_rue'),
                'to': (),
            },
        },
    },

    'DEPOSIT EVENT':
    {
        'factory': [mappers.UrbanEventFactory],

        'mappers': {
            mappers.DepositEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            mappers.DepositDateMapper: {
                'from': 'DEPOT',
                'to': 'eventDate',
            },

            mappers.EventCompletionStateMapper: {
                'from': (),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },
        },
    },

    'TASKS':
    {
        'factory': [mappers.TaskFactory],

        'mappers': {
            mappers.TaskTableMapper: {
                'table': 'courrier',
                'KEYS': ('DOSSIER', 'dossier'),
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
                        'from': ('Remarques', 'Destinataire', 'Expéditeur', 'Expédition', 'Gestionnaire'),
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
}