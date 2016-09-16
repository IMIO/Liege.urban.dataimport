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
    DecisionDateMapper, DecisionMapper


OBJECTS_NESTING = [
    ('LICENCE', [
        ('PERSON CONTACT', []),
        ('CORPORATION CONTACT', []),
        ('DEPOSIT EVENT', []),
        ('INQUIRY EVENT', [
            ('CLAIMANTS', []),
        ]),
        ('DECISION COLLEGE EVENT', []),
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
                'from': 'NUMDOSSIERBKP',
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

            ArchitectMapper: {
                'from': 'NUMARCHITECTE',
                'to': 'architects',
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
                'from': 'NB_LOG',
                'to': ('noApplication', 'habitationsAfterLicence'),
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

    'INQUIRY EVENT':
    {
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

    'DECISION COLLEGE EVENT':
    {
        'factory': [UrbanEventFactory],

        'mappers': {
            DecisionEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            DecisionDateMapper: {
                'from': 'COLLDEFINITIF1',
                'to': 'decisionDate',
            },

            DecisionMapper: {
                'from': 'COLLDECISION',
                'to': 'investigationEnd',
            },
        },
    },
}
