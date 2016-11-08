# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.mapper import AccessSimpleMapper as SimpleMapper

from Liege.urban.dataimport.buildlicence.mappers import LicenceFactory, \
    TypeAndCategoryMapper, ReferenceMapper, CompletionStateMapper, ErrorsMapper, \
    FolderCategoryMapper, ContactFactory, ContactTitleMapper, ContactNameMapper, \
    ContactStreetMapper, ContactIdMapper, LocalityMapper, CorporationIdMapper, \
    CorporationNameMapper, CorporationFactory, ArchitectMapper, UrbanEventFactory, \
    DepositEventMapper, DepositDateMapper, AnnoncedDelayMapper, InquiryEventMapper, \
    InquiryStartDateMapper, InquiryEndDateMapper, InquiryExplainationDateMapper, \
    ClaimantTableMapper, ClaimantIdMapper, ClaimantTitleMapper, ClaimantNameMapper, \
    ClaimantStreetMapper, ClaimantLocalityMapper, ClaimantFactory, ClaimDateMapper, \
    HabitationMapper, InquiryDetailsMapper, ArticleTextMapper, DecisionEventMapper, \
    DecisionDateMapper, DecisionMapper, OpinionRequestEventFactory, OpinionRequestMapper, \
    OpinionEventTypeMapper, OpinionTransmitDateMapper, OpinionReceiptDateMapper, \
    OpinionMapper, OpinionTitleMapper, OpinionIdMapper, SolicitOpinionsMapper, \
    TaskFactory, TaskTableMapper, TaskIdMapper, TaskDateMapper, TaskDescriptionMapper, \
    NotificationDateMapper, FirstCollegeDateMapper, FirstCollegeEventMapper, \
    SecondCollegeDateMapper, SecondCollegeEventMapper, FirstCollegeDecisionMapper, \
    SecondCollegeDecisionMapper, OldAddressMapper, WorklocationsMapper, \
    OldAddressNumberMapper, AddressFactory, AddressPointMapper, ParcelsMapper, \
    CapakeyMapper, DescriptionMapper, DecisionEventTitleMapper, SecondDepositEventMapper, \
    SecondDepositDateMapper, InspectionTaskTitle, InspectionTaskIdMapper, ArchiveTaskTitle, \
    ArchiveTaskIdMapper, ArchiveTaskDateMapper, DeclarationDecisionDateMapper, \
    NotificationEventMapper, DeclarationNotificationDateMapper, FDResponseEventMapper, \
    FDTransmitDateMapper, FDAnswerReceiptDateMapper, FDOpinionMapper, InspectionTaskDateMapper, \
    PEBMapper


OBJECTS_NESTING = [
    ('LICENCE', [
        ('PERSON CONTACT', []),
        ('CORPORATION CONTACT', []),
        ('ADDRESS POINT', []),
        ('PARCELS', []),
        ('DEPOSIT EVENT', []),
        ('SECOND DEPOSIT EVENT', []),
        ('INQUIRY EVENT', [
            ('CLAIMANTS', []),
        ]),
        ('OPINION REQUEST EVENT', []),
        ('FD FIRST COLLEGE EVENT', []),
        ('FD SECOND COLLEGE EVENT', []),
        ('FD RESPONSE EVENT', []),
        ('BUILDLICENCE DECISION COLLEGE EVENT', []),
        ('DECLARATION DECISION COLLEGE EVENT', []),
        ('DECLARATION NOTIFICATION EVENT', []),
        ('TASKS', []),
        ('ARCHIVE TASK', []),
        ('INSPECTION TASK', []),
    ],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [LicenceFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'NUMDOSSIERBKP',
                    'to': 'id',
                },
                {
                    'from': 'Objettrav',
                    'to': 'licenceSubject',
                },
                {
                    'from': 'UPNumero',
                    'to': 'referenceDGATLP',
                },
            ),

            TypeAndCategoryMapper: {
                'from': 'NORM_UNIK',
                'to': ('portal_type', 'foldercategory'),
            },

            ReferenceMapper: {
                'from': ('NUMDOSSIERBKP', 'NORM_UNIK'),
                'to': 'reference',
            },

            FolderCategoryMapper: {
                'from': 'CODE NAT TRAVAUX',
                'to': 'folderCategoryTownship',
            },

            AnnoncedDelayMapper: {
                'from': 'Délai',
                'to': 'annoncedDelay',
            },

            OldAddressMapper: {
                'table': 'Rues',
                'KEYS': ('Correspondance_adr', 'Numero'),
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

            ArchitectMapper: {
                'from': 'NUMARCHITECTE',
                'to': 'architects',
            },

            PEBMapper: {
                'from': (
                    'PEB_dateengag',
                    'PEB_engag_comm',
                    'PEB_datefinal',
                    'PEB_final_comm',
                    'PEB_RW',
                    'PEB_dateEngageDem',
                    'PEB_dateEngageDemComm',
                ),
                'to': 'pebDetails',
            },

            SolicitOpinionsMapper: {
                'table': 'TA Avis_services',
                'KEYS': ('NUMERO DE DOSSIER', 'Avis_services'),
                'from': ('Nom_service', 'NUMERO DE DOSSIER', 'NORM_UNIK'),
                'to': 'solicitOpinionsTo',
            },

            InquiryDetailsMapper: {
                'table': 'T Publicites',
                'KEYS': ('NUMERO DE DOSSIER', 'DOSSIER'),
                'mappers': {
                    SimpleMapper: (
                        {
                            'from': 'carac2',
                            'to': 'derogationDetails',
                        },
                    ),

                    ArticleTextMapper: {
                        'from': 'carac1',
                        'to': 'investigationArticlesText',
                    },
                }
            },

            HabitationMapper: {
                'from': ('NB_LOG', 'NB_LOG_AUTORISES', 'NB_LOG_DECLARES'),
                'to': (
                    'noApplication',
                    'additionalHabitationsAsked',
                    'additionalHabitationsGiven',
                    'habitationsAfterLicence',
                ),
            },

            DescriptionMapper: {
                'from': ('NOMBRE DE PLANS', 'Ajourne2'),
                'to': ('description',),
            },

            CompletionStateMapper: {
                'from': 'COLLDECISION',
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
                    'from': 'NUM_TEL_DEMANDEUR',
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
                'from': 'CP LOCALITE DEM',
                'to': ('city', 'zipcode'),
            }
        },
    },

    'CORPORATION CONTACT':
    {
        'factory': [CorporationFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'NUM_TEL_DEMANDEUR',
                    'to': 'phone',
                },
            ),

            CorporationIdMapper: {
                'from': ('QUALITE', 'NOM DU DEMANDEUR'),
                'to': 'id',
            },

            CorporationNameMapper: {
                'from': ('QUALITE', 'NOM DU DEMANDEUR'),
                'to': ('denomination', 'legalForm'),
            },

            ContactStreetMapper: {
                'from': 'ADRESSE DEMANDEUR',
                'to': ('street', 'number'),
            },

            LocalityMapper: {
                'from': 'CP LOCALITE DEM',
                'to': ('city', 'zipcode'),
            }
        },
    },

    'ADDRESS POINT':
    {
        'factory': [AddressFactory],

        'mappers': {
            AddressPointMapper: {
                'from': ('gidptadresse', 'CAPAKEY'),
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
                'KEYS': ('NUMERO DE DOSSIER', 'NUMDOSSIER'),
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

    'SECOND DEPOSIT EVENT':
    {
        'factory': [UrbanEventFactory],

        'mappers': {
            SecondDepositEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            SecondDepositDateMapper: {
                'from': 'Date_accuse2',
                'to': 'eventDate',
            },
        },
    },

    'INQUIRY EVENT':
    {
        'allowed_containers': ['BuildLicence', 'Article127'],

        'factory': [UrbanEventFactory],

        'mappers': {
            InquiryEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            InquiryStartDateMapper: {
                'from': 'DébutPUB',
                'to': 'investigationStart',
            },

            InquiryEndDateMapper: {
                'from': 'FinPUB',
                'to': 'investigationEnd',
            },

            InquiryExplainationDateMapper: {
                'from': 'DateBU',
                'to': 'explanationStartSDate',
            },
        },
    },

    'CLAIMANTS':
    {
        'factory': [ClaimantFactory],

        'mappers': {
            ClaimantTableMapper: {
                'table': 'TA _reclamations',
                'KEYS': ('NUMERO DE DOSSIER', 'Dossier'),
                'mappers': {
                    SimpleMapper: (
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

                    ClaimantNameMapper: {
                        'from': 'Reclamant',
                        'to': ('name1', 'name2'),
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

    'OPINION REQUEST EVENT':
    {
        'factory': [OpinionRequestEventFactory],

        'mappers': {
            OpinionRequestMapper: {
                'table': 'TA Avis_services',
                'KEYS': ('NUMERO DE DOSSIER', 'Avis_services'),
                'mappers': {
                    OpinionEventTypeMapper: {
                        'from': 'Nom_service',
                        'to': 'eventtype',
                    },

                    OpinionIdMapper: {
                        'from': 'Nom_service',
                        'to': 'id',
                    },

                    OpinionTitleMapper: {
                        'from': 'Nom_service',
                        'to': 'Title',
                    },

                    OpinionTransmitDateMapper: {
                        'from': 'Date demande',
                        'to': ('eventDate', 'transmitDate'),
                    },

                    OpinionReceiptDateMapper: {
                        'from': 'Date réception',
                        'to': 'receiptDate',
                    },

                    OpinionMapper: {
                        'from': 'Service_avis',
                        'to': ('externalDecision', 'opinionText'),
                    },
                },
            }
        }
    },

    'FD FIRST COLLEGE EVENT':
    {
        'allowed_containers': ['BuildLicence', 'Article127'],

        'factory': [UrbanEventFactory],

        'mappers': {
            FirstCollegeEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            FirstCollegeDateMapper: {
                'from': 'College2',
                'to': 'eventDate',
            },

            FirstCollegeDecisionMapper: {
                'from': ('College/Fav/Def', 'Ajourne2'),
                'to': 'decision',
            },
        },
    },

    'FD SECOND COLLEGE EVENT':
    {
        'allowed_containers': ['BuildLicence', 'Article127'],

        'factory': [UrbanEventFactory],

        'mappers': {
            SecondCollegeEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            SecondCollegeDateMapper: {
                'from': 'College3',
                'to': 'eventDate',
            },

            SecondCollegeDecisionMapper: {
                'from': 'College/Fav/Def2',
                'to': 'decision',
            },
        },
    },

    'FD RESPONSE EVENT':
    {
        'allowed_containers': ['BuildLicence', 'Article127'],

        'factory': [UrbanEventFactory],

        'mappers': {
            FDResponseEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            FDTransmitDateMapper: {
                'from': 'UP2',
                'to': 'eventDate',
            },

            FDAnswerReceiptDateMapper: {
                'from': 'UP3',
                'to': 'receiptDate',
            },

            FDOpinionMapper: {
                'from': 'Avis',
                'to': ('externalDecision', 'opinionText'),
            },
        },
    },

    'BUILDLICENCE DECISION COLLEGE EVENT':
    {
        'allowed_containers': ['BuildLicence', 'Article127'],

        'factory': [UrbanEventFactory],

        'mappers': {
            DecisionEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            DecisionEventTitleMapper: {
                'from': 'DecisionFinaleUP',
                'to': 'title',
            },

            NotificationDateMapper: {
                'from': 'notification',
                'to': 'eventDate',
            },

            DecisionDateMapper: {
                'from': 'COLLDEFINITIF1',
                'to': 'decisionDate',
            },

            DecisionMapper: {
                'from': 'COLLDECISION',
                'to': 'decision',
            },
        },
    },

    'DECLARATION DECISION COLLEGE EVENT':
    {
        'allowed_containers': ['Declaration'],

        'factory': [UrbanEventFactory],

        'mappers': {
            DecisionEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            DecisionEventTitleMapper: {
                'from': 'DecisionFinaleUP',
                'to': 'title',
            },

            DeclarationDecisionDateMapper: {
                'from': 'COLLDEFINITIF1',
                'to': 'eventDate',
            },
        },
    },

    'DECLARATION NOTIFICATION EVENT':
    {
        'allowed_containers': ['Declaration'],

        'factory': [UrbanEventFactory],

        'mappers': {
            NotificationEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            DeclarationNotificationDateMapper: {
                'from': 'notification',
                'to': 'eventDate',
            },
        },
    },

    'TASKS':
    {
        'factory': [TaskFactory],

        'mappers': {
            TaskTableMapper: {
                'table': 'Courrier',
                'KEYS': ('NUMERO DE DOSSIER', 'Dossier'),
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

    'INSPECTION TASK':
    {
        'factory': [TaskFactory],

        'mappers': {
            InspectionTaskTitle: {
                'from': (),
                'to': 'title',
            },
            InspectionTaskIdMapper: {
                'from': (),
                'to': 'id',
            },
            InspectionTaskDateMapper: {
                'from': 'dateIB',
                'to': 'due_date',
            }
        },
    },

    'ARCHIVE TASK':
    {
        'factory': [TaskFactory],

        'mappers': {
            ArchiveTaskTitle: {
                'from': (),
                'to': 'title',
            },
            ArchiveTaskIdMapper: {
                'from': (),
                'to': 'id',
            },
            ArchiveTaskDateMapper: {
                'from': 'ARCH/Cad',
                'to': 'due_date',
            }
        },
    },
}
