# -*- coding: utf-8 -*-

from imio.urban.dataimport.csv.mapper import CSVSimpleMapper as SimpleMapper
from imio.urban.dataimport.factory import UrbanEventFactory

from Liege.urban.dataimport.inspection import mappers


OBJECTS_NESTING = [
    ('LICENCE', [
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
                'table': 'Rues',
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

            mappers.ErrorsMapper: {
                'from': (),
                'to': ('description',),  # log all the errors in the description field
            }
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
        },
    },

    'FOLLOWUP EVENT':
    {
        'factory': [UrbanEventFactory],

        'mappers': {

            mappers.FollowupsMapper: {
                'table': 'TA_suite_rapport_ib',
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
                        'from': ('pièce', 'encodeur', 'suite'),
                        'to': 'misc_description',
                    },
                }
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
        },
    },
}
