# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.mapper import CSVSimpleMapper as SimpleMapper
from imio.urban.dataimport.factory import UrbanEventFactory

from Liege.urban.dataimport.inspection import mappers


OBJECTS_NESTING = [
    ('LICENCE', [
        ('ADDRESS POINT', []),
        ('PROPRIETARY', []),
        ('REPORT EVENT', []),
        ('FOLLOWUP EVENT', []),
        ('COMMENT EVENT', []),
    ],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [mappers.InspectionFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'N°',
                    'to': 'id',
                },
            ),

            mappers.PortalTypeMapper: {
                'from': (),
                'to': 'portal_type',
            },

            mappers.ReferenceMapper: {
                'from': 'numerorapport',
                'to': 'reference',
            },

            mappers.FoldermanagersMapper: {
                'from': 'ref_inspecteur',
                'to': 'foldermanagers',
            },

            mappers.OldAddressMapper: {
                'table': 'Rues_inspection',
                'KEYS': ('ref_rue', 'Numero'),
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

            mappers.ComplaintTableMapper: {
                'table': 'INSP_RAPPORT_data5',
                'KEYS': ('N°', 'N°'),
                'mappers': {
                    mappers.ComplaintTextMapper: {
                        'from': 'plainte',
                        'to': 'inspectionDescription',
                    },
                }
            },

            mappers.InfosTableMapper: {
                'table': 'INSP_RAPPORT_data6',
                'KEYS': ('N°', 'N°'),
                'mappers': {
                    mappers.InfosTextMapper: {
                        'from': 'infos',
                        'to': 'description',
                    },
                }
            },

            mappers.CompletionStateMapper: {
                'from': (),
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

            mappers.InspectionAddressPointTableMapper: {
                'table': 'INSPBATI_PlusieursPtadresses',
                'KEYS': ('N°', 'N'),
                'mappers': {
                    mappers.AdditionalAddressPointMapper: {
                        'from': 'gidnum',
                        'to': (),
                    },
                }
            },
        },
    },

    'PROPRIETARY':
    {
        'factory': [mappers.ProprietaryFactory],
        'mappers': {
            SimpleMapper: (
                {
                    'from': 'proprio',
                    'to': 'name1',
                },
            ),

            mappers.ContactIdMapper: {
                'from': 'proprio',
                'to': 'id',
            },

            mappers.ContactAddressTableMapper: {
                'table': 'INSP_RAPPORT_data2',
                'KEYS': ('N°', 'N°'),
                'mappers': {

                    mappers.ContactAddressMapper: {
                        'from': 'adr_proprio',
                        'to': ('street', 'number', 'zipcode', 'city'),
                    },
                }
            },
        },
    },

    'REPORT EVENT':
    {
        'factory': [UrbanEventFactory],

        'mappers': {
            mappers.ReportEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            mappers.InspectDateMapper: {
                'from': 'date_constat',
                'to': 'eventDate',
            },

            mappers.ReportDateMapper: {
                'from': 'date_rapport',
                'to': 'reportDate',
            },

            mappers.ReportTableMapper: {
                'table': 'INSP_RAPPORT_data3',
                'KEYS': ('N°', 'N°'),
                'mappers': {
                    mappers.ReportTextMapper: {
                        'from': 'rapport',
                        'to': 'report',
                    },
                }
            },

            mappers.ArticlesTableMapper: {
                'table': 'INSP_RAPPORT_data4',
                'KEYS': ('N°', 'N°'),
                'mappers': {
                    mappers.ArticleTextMapper: {
                        'from': 'ref_cwatup',
                        'to': 'offense_articles_details',
                    },
                }
            },

            mappers.EventCompletionStateMapper: {
                'from': (),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },
        },
    },

    'FOLLOWUP EVENT':
    {
        'factory': [UrbanEventFactory],

        'mappers': {

            mappers.FollowupsMapper: {
                'table': 'INSP_TA_suite_rapport_ib',
                'KEYS': ('numerorapport', 'num_rapport'),
                'mappers': {

                    mappers.FollowupEventMapper: {
                        'from': (),
                        'to': 'eventtype',
                    },

                    mappers.FollowupDateMapper: {
                        'from': 'date_encodage',
                        'to': 'eventDate',
                    },

                    mappers.FollowupMapper: {
                        'from': ('piece', 'encodeur', 'suite'),
                        'to': 'misc_description',
                    },
                }
            },

            mappers.EventCompletionStateMapper: {
                'from': (),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },
        },
    },

    'COMMENT EVENT':
    {
        'factory': [UrbanEventFactory],

        'mappers': {
            mappers.CommentEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            mappers.CommentsMapper: {
                'table': 'INSP_RAPPORT_data7',
                'KEYS': ('N°', 'N°'),
                'mappers': {
                    mappers.CommentMapper: {
                        'from': ('commentaires'),
                        'to': 'misc_description',
                    },
                }
            },

            mappers.EventCompletionStateMapper: {
                'from': (),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },
        },
    },
}
