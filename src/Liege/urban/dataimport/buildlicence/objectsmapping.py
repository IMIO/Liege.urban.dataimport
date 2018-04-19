# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.mapper import CSVSimpleMapper as SimpleMapper

from Liege.urban.dataimport.buildlicence.mappers import LicenceFactory, \
    TypeAndCategoryMapper, ReferenceMapper, CompletionStateMapper, ErrorsMapper, \
    FolderCategoryMapper, ContactFactory, ContactTitleMapper, \
    ContactStreetMapper, LocalityMapper, RecourseDateMapper, RecourseDescriptionMapper, \
    CorporationNameMapper, CorporationFactory, ArchitectMapper, UrbanEventFactory, \
    DepositEventMapper, DepositDateMapper, AnnoncedDelayMapper, InquiryEventMapper, \
    InquiryStartDateMapper, InquiryEndDateMapper, InquiryExplainationDateMapper, \
    ClaimantTableMapper, ClaimantIdMapper, ClaimantTitleMapper, \
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
    PEBMapper, DeclarationDecisionEventMapper, ApplicantMapper, RecourseTransmitDateMapper, \
    RecourseEventMapper, IdMapper, ContactIdMapper, Clean127LicencesMapper


OBJECTS_NESTING = [
    ('LICENCE', [
#        ('PERSON CONTACT', []),
#        ('CORPORATION CONTACT', []),
#        ('ADDRESS POINT', []),
#        ('PARCELS', []),
#        ('DEPOSIT EVENT', []),
#        ('SECOND DEPOSIT EVENT', []),
#        ('INQUIRY EVENT', [
#            ('CLAIMANTS', []),
#        ]),
#        ('OPINION REQUEST EVENT', []),
        ('FD FIRST COLLEGE EVENT', []),
        ('FD SECOND COLLEGE EVENT', []),
        ('FD RESPONSE EVENT', []),
        ('BUILDLICENCE DECISION COLLEGE EVENT', []),
#        ('BUILDLICENCE NOTIFICATION EVENT', []),
#        ('DECLARATION DECISION COLLEGE EVENT', []),
#        ('DECLARATION NOTIFICATION EVENT', []),
#        ('RECOURSE EVENT', []),
#        ('TASKS', []),
#        ('ARCHIVE TASK', []),
#        ('INSPECTION TASK', []),
    ],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [LicenceFactory],

        'mappers': {
#            SimpleMapper: (
#                {
#                    'from': 'Objettrav',
#                    'to': 'licenceSubject',
#                },
#                {
#                    'from': 'UPNumero',
#                    'to': 'referenceDGATLP',
#                },
#            ),

            IdMapper: {
                'from': 'NUMERO DE DOSSIER',
                'to': 'id',
            },

            Clean127LicencesMapper: {
                'from': (
                    'NUMERO DE DOSSIER',
                    'College2', 'College3',
                    'UP2', 'UP3',
                    'COLLDEFINITIF1'
                ),
                'to': (),
            },

            TypeAndCategoryMapper: {
                'from': 'NORM_UNIK',
                'to': ('portal_type', 'foldercategory'),
            },

#            ReferenceMapper: {
#                'from': ('NUMERO DE DOSSIER', 'NORM_UNIK'),
#                'to': 'reference',
#            },

#            FolderCategoryMapper: {
#                'from': 'CODE NAT TRAVAUX',
#                'to': 'folderCategoryTownship',
#            },

#            AnnoncedDelayMapper: {
#                'from': 'Délai',
#                'to': 'annoncedDelay',
#            },

#            OldAddressMapper: {
#                'table': 'Rues',
#                'KEYS': ('Correspondance_adr', 'Numero'),
#                'mappers': {
#                    WorklocationsMapper: {
#                        'from': ('CODE_RUE', 'Localite', 'PARTICULE', 'RUE'),
#                        'to': 'workLocations',
#                    },
#                }
#            },

#            OldAddressNumberMapper: {
#                'from': ('NUM', 'Num2'),
#                'to': 'workLocations',
#            },

#            ArchitectMapper: {
#                'from': 'NUMARCHITECTE',
#                'to': 'architects',
#            },

#            PEBMapper: {
#                'from': (
#                    'PEB_dateengag',
#                    'PEB_engag_comm',
#                    'PEB_datefinal',
#                    'PEB_final_comm',
#                    'PEB_RW',
#                    'PEB_dateEngageDem',
#                    'PEB_dateEngageDemComm',
#                ),
#                'to': 'pebDetails',
#            },

#            SolicitOpinionsMapper: {
#                'table': 'TA Avis_services',
#                'KEYS': ('NUMERO DE DOSSIER', 'Avis_services'),
#                'from': ('Nom_service', 'NUMERO DE DOSSIER', 'NORM_UNIK'),
#                'to': 'solicitOpinionsTo',
#            },

#            InquiryDetailsMapper: {
#                'table': 'T Publicites',
#                'KEYS': ('NUMERO DE DOSSIER', 'DOSSIER'),
#                'mappers': {
#                    SimpleMapper: (
#                        {
#                            'from': 'carac2',
#                            'to': 'derogationDetails',
#                        },
#                    ),

#                    ArticleTextMapper: {
#                        'from': 'carac1',
#                        'to': 'investigationArticlesText',
#                    },
#                }
#            },

#            HabitationMapper: {
#                'from': ('NB_LOG', 'NB_LOG_AUTORISES', 'NB_LOG_DECLARES'),
#                'to': (
#                    'noApplication',
#                    'additionalHabitationsAsked',
#                    'additionalHabitationsGiven',
#                    'habitationsAfterLicence',
#                ),
#            },

#            DescriptionMapper: {
#                'from': ('NOMBRE DE PLANS', 'Ajourne2'),
#                'to': ('description',),
#            },

#            CompletionStateMapper: {
#                'from': ('Délai', 'Date_accuse2', 'COLLDEFINITIF1', 'notification', 'COLLDECISION'),
#                'to': (),  # <- no field to fill, its the workflow state that has to be changed
#            },

#            ErrorsMapper: {
#                'from': (),
#                'to': ('description',),  # log all the errors in the description field
#            }
        },
    },

    'PERSON CONTACT':
    {
        'factory': [ContactFactory],
        'mappers': {
            ApplicantMapper: {
                'table': 'DEMANDEURS_PURBA',
                'KEYS': ('NUMERO DE DOSSIER', 'NUMERO DE DOSSIER'),
                'mappers': {
                    SimpleMapper: (
                        {
                            'from': 'NOMDEMANDEUR',
                            'to': 'name1',
                        },
                        {
                            'from': 'NUMTELDEM',
                            'to': 'phone',
                        },
                    ),

                    ContactIdMapper: {
                        'from': 'NOMDEMANDEUR',
                        'to': 'id',
                    },

                    ContactTitleMapper: {
                        'from': 'QUALITE',
                        'to': 'personTitle',
                    },

                    ContactStreetMapper: {
                        'from': 'ADRESSEDEMANDEUR',
                        'to': ('street', 'number'),
                    },

                    LocalityMapper: {
                        'from': 'CPLOCALITEDEM',
                        'to': ('city', 'zipcode'),
                    }
                },
            },
        },
    },


    'CORPORATION CONTACT':
    {
        'factory': [CorporationFactory],
        'mappers': {
            ApplicantMapper: {
                'table': 'DEMANDEURS_PURBA',
                'KEYS': ('NUMERO DE DOSSIER', 'NUMERO DE DOSSIER'),
                'mappers': {
                    SimpleMapper: (
                        {
                            'from': 'NUMTELDEM',
                            'to': 'phone',
                        },
                    ),

                    ContactIdMapper: {
                        'from': 'NOMDEMANDEUR',
                        'to': 'id',
                    },

                    CorporationNameMapper: {
                        'from': ('QUALITE', 'NOMDEMANDEUR'),
                        'to': ('denomination', 'legalForm'),
                    },

                    ContactStreetMapper: {
                        'from': 'ADRESSEDEMANDEUR',
                        'to': ('street', 'number'),
                    },

                    LocalityMapper: {
                        'from': 'CPLOCALITEDEM',
                        'to': ('city', 'zipcode'),
                    }
                },
            },
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
                'KEYS': ('NUMERO DE DOSSIER', 'NUMERO DE DOSSIER'),
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
        'allowed_containers': ['BuildLicence', 'Article127', 'UniqueLicence', 'IntegratedLicence'],

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

    'OPINION REQUEST EVENT':
    {
        'allowed_containers': ['BuildLicence', 'Article127', 'UniqueLicence', 'IntegratedLicence'],

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
                        'from': ('Nom_service', 'Date demande', 'Date réception'),
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
                'to': ('eventDate', 'decisionDate'),
            },

            FirstCollegeDecisionMapper: {
                'from': ('College/Fav/Def', 'Ajourne'),
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
                'to': ('eventDate', 'decisionDate'),
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
        'allowed_containers': ['BuildLicence', 'Article127', 'UniqueLicence', 'IntegratedLicence'],

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

            DecisionDateMapper: {
                'from': 'COLLDEFINITIF1',
                'to': ('eventDate', 'decisionDate'),
            },

            DecisionMapper: {
                'from': 'COLLDECISION',
                'to': 'decision',
            },
        },
    },

    'BUILDLICENCE NOTIFICATION EVENT':
    {
        'allowed_containers': ['BuildLicence', 'Article127', 'UniqueLicence', 'IntegratedLicence'],

        'factory': [UrbanEventFactory],

        'mappers': {
            NotificationEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            NotificationDateMapper: {
                'from': 'notification',
                'to': ('eventDate', 'transmitDate')
            },
        },
    },

    'DECLARATION DECISION COLLEGE EVENT':
    {
        'allowed_containers': ['Declaration'],

        'factory': [UrbanEventFactory],

        'mappers': {
            DeclarationDecisionEventMapper: {
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
                'to': ('eventDate', 'transmitDate'),
            },
        },
    },

    'RECOURSE EVENT':
    {
        'factory': [UrbanEventFactory],

        'mappers': {
            TaskTableMapper: {
                'table': 'TA_Recours',
                'KEYS': ('NUMERO DE DOSSIER', 'Dossier'),
                'mappers': {
                    SimpleMapper: (
                        {
                            'from': 'Objet',
                            'to': 'Title',
                        },
                    ),
                    RecourseEventMapper: {
                        'from': (),
                        'to': 'eventtype',
                    },
                    TaskIdMapper: {
                        'from': 'numpiece',
                        'to': 'id',
                    },
                    RecourseDateMapper: {
                        'from': 'Date',
                        'to': 'eventDate',
                    },
                    RecourseTransmitDateMapper: {
                        'from': 'Expédition',
                        'to': 'transmitDate',
                    },
                    RecourseDescriptionMapper: {
                        'from': ('remarques', 'Destinataire', 'Expéditeur', 'Gestionnaire', 'Pelure'),
                        'to': 'decisionText',
                    },
                }
            }
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
