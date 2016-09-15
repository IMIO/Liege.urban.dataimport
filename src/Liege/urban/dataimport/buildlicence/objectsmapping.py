# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.mapper import AccessSimpleMapper as SimpleMapper

from Liege.urban.dataimport.buildlicence.mappers import LicenceFactory, \
    TypeAndCategoryMapper, ReferenceMapper, CompletionStateMapper, ErrorsMapper, \
    FolderCategoryMapper, ContactFactory, ContactTitleMapper, ContactNameMapper, \
    ContactStreetMapper, ContactIdMapper, LocalityMapper, CorporationIdMapper, \
    CorporationNameMapper, CorporationFactory, ArchitectMapper, UrbanEventFactory, \
    DepositEventMapper, DepositDateMapper, AnnoncedDelayMapper, InquiryEventMapper, \
    InquiryStartDateMapper, InquiryEndDateMapper, InquiryExplainationDateMapper


OBJECTS_NESTING = [
    (
        'LICENCE', [
            ('PERSON CONTACT', []),
            ('CORPORATION CONTACT', []),
            ('DEPOSIT EVENT', []),
            ('INQUIRY EVENT', []),
        ],
    ),
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
}
