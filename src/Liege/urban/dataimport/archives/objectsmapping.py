 #-*- coding: utf-8 -*-

from imio.urban.dataimport.access.mapper import AccessSimpleMapper as SimpleMapper
from imio.urban.dataimport.factory import UrbanEventFactory

from Liege.urban.dataimport.archives.mappers import LicenceFactory
from Liege.urban.dataimport.archives.mappers import LicenceSubjectMapper
from Liege.urban.dataimport.archives.mappers import WorklocationsMapper
from Liege.urban.dataimport.archives.mappers import StreetTableMapper
from Liege.urban.dataimport.archives.mappers import StreetNumberMapper
from Liege.urban.dataimport.archives.mappers import OldLocationMapper
from Liege.urban.dataimport.archives.mappers import CompletionStateMapper
from Liege.urban.dataimport.archives.mappers import ErrorsMapper
from Liege.urban.dataimport.archives.mappers import ContactFactory
from Liege.urban.dataimport.archives.mappers import ContactIdMapper
from Liege.urban.dataimport.archives.mappers import DecisionEventMapper
from Liege.urban.dataimport.archives.mappers import DecisionDateMapper
from Liege.urban.dataimport.archives.mappers import EventCompletionStateMapper


OBJECTS_NESTING = [
    ('LICENCE', [
        ('PERSON CONTACT', []),
        ('BUILDLICENCE DECISION COLLEGE EVENT', []),
    ],),
]

FIELDS_MAPPINGS = {
    'LICENCE':
    {
        'factory': [LicenceFactory],

        'mappers': {
            SimpleMapper: (
                {
                    'from': 'Numéro',
                    'to': 'id',
                },
                {
                    'from': 'Dossier',
                    'to': 'reference',
                },
            ),

            LicenceSubjectMapper: {
                'table': 'TA Objets_arch',
                'KEYS': ('Nature Travaux', 'Code'),
                'mappers': {
                    SimpleMapper: (
                        {
                            'from': 'Objet_travaux',
                            'to': 'licenceSubject',
                        },
                    ),
                }
            },

            StreetTableMapper: {
                'from': ('ref_rue', 'Code National de la rue', 'Code Postal', 'ADRESSE'),
                'table': 'Rues',
                'KEYS': ('ref_rue', 'Numero'),
                'mappers': {
                    WorklocationsMapper: {
                        'from': ('Code National de la rue', 'Code Postal', 'ADRESSE'),
                        'to': 'workLocations',
                    },
                }
            },

            StreetNumberMapper: {
                'from': ('NumPol', 'Rue', 'Particule'),
                'to': (),
            },

            OldLocationMapper: {
                'from': ('Repère1', 'Repère1b', 'Repère3', 'AncienNomRue'),
                'to': ('description'),
            },

            CompletionStateMapper: {
                'from': (),
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
                    'from': 'Propriétaire',
                    'to': 'name1',
                },
            ),

            ContactIdMapper: {
                'from': 'Propriétaire',
                'to': 'id',
            },
        },
    },

    'BUILDLICENCE DECISION COLLEGE EVENT':
    {
        'factory': [UrbanEventFactory],

        'mappers': {
            DecisionEventMapper: {
                'from': (),
                'to': 'eventtype',
            },

            DecisionDateMapper: {
                'from': 'Date',
                'to': 'eventDate',
            },

            EventCompletionStateMapper: {
                'from': (),
                'to': (),  # <- no field to fill, its the workflow state that has to be changed
            },
        },
    },

}
