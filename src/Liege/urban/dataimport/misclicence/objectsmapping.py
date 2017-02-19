# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.mapper import AccessSimpleMapper as SimpleMapper

from Liege.urban.dataimport.misclicence.mappers import LicenceFactory, \
    PortalTypeMapper, ReferenceMapper, CompletionStateMapper, ErrorsMapper, \
    ContactFactory, ContactTitleMapper, ContactNameMapper, IdMapper, \
    ContactStreetMapper, ContactIdMapper, LocalityMapper, UrbanEventFactory, \
    DepositEventMapper, DepositDateMapper, DecisionEventMapper, DecisionDateMapper, \
    TaskFactory, TaskTableMapper, TaskIdMapper, TaskDateMapper, TaskDescriptionMapper, \
    FirstCollegeDateMapper, FirstCollegeEventMapper, FirstCollegeDecisionMapper, \
    OldAddressMapper, WorklocationsMapper, DecisionMapper, \
    OldAddressNumberMapper, AddressFactory, AddressPointMapper, ParcelsMapper, \
    CapakeyMapper, FDResponseEventMapper, \
    FDAnswerReceiptDateMapper, FDOpinionMapper


OBJECTS_NESTING = [
    ('LICENCE', [
        ('PERSON CONTACT', []),
        ('ADDRESS POINT', []),
        ('PARCELS', []),
        ('DEPOSIT EVENT', []),
        ('CU FIRST COLLEGE EVENT', []),
        ('FD RESPONSE EVENT', []),
        ('CU DECISION COLLEGE EVENT', []),
        ('TASKS', []),
    ],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [LicenceFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'Objettrav',
                    'to': 'licenceSubject',
                },
            ),

            IdMapper: {
                'from': 'DOSSIER',
                'to': 'id',
            },

            PortalTypeMapper: {
                'from': ('Type_trav', 'COLLEGE_DECISION'),
                'to': 'portal_type',
            },

            ReferenceMapper: {
                'from': ('DOSSIER', 'Type_trav', 'COLLEGE_DECISION'),
                'to': 'reference',
            },

            OldAddressMapper: {
                'table': 'Rues',
                'KEYS': ('Correspondance_rue', 'Numero'),
                'mappers': {
                    WorklocationsMapper: {
                        'from': ('CODE_RUE', 'Localite', 'PARTICULE', 'RUE'),
                        'to': 'workLocations',
                    },
                }
            },

            OldAddressNumberMapper: {
                'from': ('NUM', 'Num2'),
                'to': 'workLocations',
            },

            CompletionStateMapper: {
                'from': 'COLLEGE_DECISION',
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },

            ErrorsMapper: {
                'from': (),
                'to': ('description',),  # log all the errors in the description field
            }
        },
    },

    'PERSON CONTACT':
    {
        'factory': [ContactFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'TELDEMANDEUR',
                    'to': 'phone',
                },
            ),

            ContactIdMapper: {
                'from': ('QUALITE', 'NOM DU DEMANDEUR'),
                'to': 'id',
            },

            ContactTitleMapper: {
                'from': 'QUALITE',
                'to': 'personTitle',
            },

            ContactNameMapper: {
                'from': 'NOM DU DEMANDEUR',
                'to': ('name1', 'name2'),
            },

            ContactStreetMapper: {
                'from': 'ADRESSE DEMANDEUR',
                'to': ('street', 'number'),
            },

            LocalityMapper: {
                'from': ('CODE POSTAL22', 'LOCALITE22'),
                'to': ('city', 'zipcode'),
            }
        },
    },

    'ADDRESS POINT':
    {
        'factory': [AddressFactory],

        'mappers': {
            AddressPointMapper: {
                'from': ('idptadresse', 'capakey'),
                'to': (),
            }
        },
    },

    'PARCELS':
    {
        'factory': [AddressFactory],

        'mappers': {
            ParcelsMapper: {
                'table': 'PRUBA_CADASTRE',
                'KEYS': ('DOSSIER', 'NUMDOSSIER'),
                'mappers': {
                    CapakeyMapper: {
                        'from': 'CAPAKEY',
                        'to': 'capakey',
                    }
                }
            },
        },
    },

    'DEPOSIT EVENT':
    {
        'factory': [UrbanEventFactory],

        'mappers': {
            DepositEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            DepositDateMapper: {
                'from': 'DEPOT',
                'to': 'eventDate',
            },
        },
    },

    'CU FIRST COLLEGE EVENT':
    {
        'allowed_containers': ['UrbanCertificateTwo'],

        'factory': [UrbanEventFactory],

        'mappers': {
            FirstCollegeEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            FirstCollegeDateMapper: {
                'from': 'DATE_COLL_APPREC',
                'to': 'eventDate',
            },

            FirstCollegeDecisionMapper: {
                'from': 'APRREC_ADM',
                'to': 'decision',
            },
        },
    },

    'FD RESPONSE EVENT':
    {
        'allowed_containers': ['UrbanCertificateTwo'],

        'factory': [UrbanEventFactory],

        'mappers': {
            FDResponseEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            FDAnswerReceiptDateMapper: {
                'from': 'DATE_FD',
                'to': 'receiptDate',
            },

            FDOpinionMapper: {
                'from': 'AVIS_FD',
                'to': ('externalDecision', 'opinionText'),
            },
        },
    },

    'CU DECISION COLLEGE EVENT':
    {
        'allowed_containers': ['UrbanCertificateTwo'],

        'factory': [UrbanEventFactory],

        'mappers': {
            DecisionEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            DecisionDateMapper: {
                'from': 'DATE_COLL_DECIS',
                'to': 'eventDate',
            },

            DecisionMapper: {
                'from': 'COLLEGE_DECISION',
                'to': 'decision',
            }
        },
    },

    'TASKS':
    {
        'factory': [TaskFactory],

        'mappers': {
            TaskTableMapper: {
                'table': 'Courrier',
                'KEYS': ('DOSSIER', 'Dossier'),
                'mappers': {
                    SimpleMapper: (
                        {
                            'from': 'Objet',
                            'to': 'title',
                        },
                    ),
                    TaskIdMapper: {
                        'from': 'numpiece',
                        'to': 'id',
                    },
                    TaskDescriptionMapper: {
                        'from': ('remarques', 'Destinataire', 'Expéditeur', 'Expédition', 'Gestionnaire'),
                        'to': 'task_description',
                    },
                    TaskDateMapper: {
                        'from': 'Date',
                        'to': 'due_date',
                    }
                }
            }
        },
    },
}
