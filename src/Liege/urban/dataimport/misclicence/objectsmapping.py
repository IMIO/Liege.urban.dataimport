# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.mapper import CSVSimpleMapper as SimpleMapper

from Liege.urban.dataimport.misclicence.mappers import LicenceFactory, \
    PortalTypeMapper, ReferenceMapper, CompletionStateMapper, ErrorsMapper, \
    ContactFactory, IdMapper, CU1SubjectMapper, InquiryExplainationDateMapper, \
    ContactStreetMapper, ContactIdMapper, LocalityMapper, UrbanEventFactory, \
    DepositEventMapper, DepositDateMapper, DecisionEventMapper, DecisionDateMapper, \
    TaskFactory, TaskTableMapper, TaskIdMapper, TaskDateMapper, TaskDescriptionMapper, \
    FirstCollegeDateMapper, FirstCollegeEventMapper, FirstCollegeDecisionMapper, \
    OldAddressMapper, WorklocationsMapper, DecisionMapper, InquiryEventMapper, \
    OldAddressNumberMapper, AddressFactory, AddressPointMapper, \
    FDResponseEventMapper, EventCompletionStateMapper, ClaimantFactory, ClaimantTableMapper, \
    FDAnswerReceiptDateMapper, FDOpinionMapper, ClaimantIdMapper, ClaimantTitleMapper, \
    ClaimantStreetMapper, ClaimantLocalityMapper, ClaimDateMapper


OBJECTS_NESTING = [
    ('LICENCE', [
        ('PERSON CONTACT', []),
        ('ADDRESS POINT', []),
        ('DEPOSIT EVENT', []),
        ('INQUIRY EVENT', [
            ('CLAIMANTS', []),
        ]),
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
                'from': ('Type_trav', 'Objettrav', 'COLLEGE_DECISION'),
                'to': 'portal_type',
            },

            ReferenceMapper: {
                'from': ('DOSSIER', 'Type_trav', 'COLLEGE_DECISION'),
                'to': 'reference',
            },

            CU1SubjectMapper: {
                'from': 'Objettrav',
                'to': 'description',
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
                {
                    'from': 'NOM DU DEMANDEUR',
                    'to': 'name1',
                },
            ),

            ContactIdMapper: {
                'from': ('QUALITE', 'NOM DU DEMANDEUR'),
                'to': 'id',
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
                'from': ('gidptadresse', 'capakey', 'Numero', 'Correspondance_rue'),
                'to': (),
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

            EventCompletionStateMapper: {
                'from': (),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },
        },
    },

    'INQUIRY EVENT':
    {
        'allowed_containers': ['UrbanCertificateTwo'],

        'factory': [UrbanEventFactory],

        'mappers': {
            InquiryEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            InquiryExplainationDateMapper: {
                'from': ('DateBU', 'DOSSIER'),
                'to': 'explanationStartSDate',
            },
        },
    },

    'CLAIMANTS':
    {
        'factory': [ClaimantFactory],

        'mappers': {
            ClaimantTableMapper: {
                'table': '_TReclamationsAffairesDiverses',
                'KEYS': ('DOSSIER', 'Dossier'),
                'mappers': {
                    SimpleMapper: (
                        {
                            'from': 'Reclamant',
                            'to': 'name1',
                        },
                        {
                            'from': 'societe',
                            'to': 'society',
                        },
                    ),

                    ClaimantIdMapper: {
                        'from': 'Reclamant',
                        'to': 'id',
                    },

                    ClaimantTitleMapper: {
                        'from': 'civilite',
                        'to': 'personTitle',
                    },

                    ClaimantStreetMapper: {
                        'from': 'adresse',
                        'to': ('street', 'number'),
                    },

                    ClaimantLocalityMapper: {
                        'from': 'CP',
                        'to': ('city', 'zipcode'),
                    },

                    ClaimDateMapper: {
                        'from': 'Date_reclam',
                        'to': 'claimDate',
                    },
                },
            },
        }
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

            EventCompletionStateMapper: {
                'from': (),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
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

            EventCompletionStateMapper: {
                'from': (),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
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
            },

            EventCompletionStateMapper: {
                'from': (),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },
        },
    },

    'TASKS':
    {
        'factory': [TaskFactory],

        'mappers': {
            TaskTableMapper: {
                'table': 'T Courr_affdiv',
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
                        'from': ('Remarques', 'Destinataire', 'Expéditeur', 'Expédition', 'Gestionnaire'),
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
