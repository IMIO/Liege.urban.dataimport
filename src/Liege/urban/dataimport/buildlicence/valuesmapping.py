# -*- coding: utf-8 -*-

from imio.urban.dataimport.mapping import table

VALUES_MAPS = {

'type_map': table({
'header'  : ['portal_type',       'foldercategory', 'abreviation'],
'N'       : ['BuildLicence',      'pn',             'PU'],
'U'       : ['UniqueLicence',     'pu',             'U'],
'M'       : ['Article127',        '',               'M'],  # Article127
'I'       : ['IntegratedLicence', 'pi',             'PI'],
'V'       : ['Article127',        '',               'V'],  # Article127
'D'       : ['Declaration',       '',               'D'],  # Declaration
''        : ['',                  '',               ''],
}),

'state_map': {
    'autorisé': 'accepted',
    'recevable': 'accepted',
    'refusé': 'refused',
    'refusé tacite': 'refused',
    'refusé par défaut': 'refused',
    'irrecevable': 'refused',
    'sans suite': 'retired',
    'abandonné': 'retired',
},

'eventtype_id_map': table({
    'header'             : ['decision_event',                       'deposit_event',       'second_deposit_event',       'notification_event'],
    'BuildLicence'       : ['delivrance-du-permis-octroi-ou-refus', 'depot-de-la-demande', 'recepisse-art15-complement', 'notification-de-la-decision'],
    'Article127'         : ['decision-du-fd-sur-127',               'reception-du-dossier-du-spw', 'recepisse-art15-complement', 'transmis-decision-aux-reclamants'],
    'Declaration'        : ['deliberation-college',                 'depot-de-la-demande', 'depot-de-la-demande',        'transmis-decision'],
    'IntegratedLicence'  : ['decision-finale', 'depot-du-dossier',  'reception-complement', 'notification-de-la-decision-doc-de-transmis'],
    'UniqueLicence'      : ['decision-finale', 'depot-du-dossier',  'reception-complement', 'notification-de-la-decision-doc-de-transmis'],
}),

'person_title_map': {
    'monsieur': 'mister',
    'm.': 'mister',
    'm': 'mister',
    'dr': 'mister',
    'me': 'mister',
    'ms': 'misters',
    'mrs': 'misters',
    'messieurs': 'misters',
    'madame': 'madam',
    'mme': 'madam',
    'mesdames': 'ladies',
    'mmes': 'ladies',
    'mesdemoiselles': 'ladies',
    'mademoiselle': 'madam',
    'melle': 'madam',
    'ms et mmes': 'madam_and_mister',
    'mr et mme': 'madam_and_mister',
    'm. et mme': 'madam_and_mister',
    'm. et mmes': 'madam_and_mister',
    'm. et mme.': 'madam_and_mister',
    'm. et melle': 'madam_and_mister',
    'mme et m.': 'madam_and_mister',
    'melle et m.': 'madam_and_mister',
    'maître': 'master',
},

'externaldecisions_map': {
    'favorable': 'favorable',
    'fav': 'favorable',
    'favorable conditionnelle': 'favorable-conditionnel',
    'favorable conditionnel': 'favorable-conditionnel',
    'fav conditionnel': 'favorable-conditionnel',
    'fav cond': 'favorable-conditionnel',
    'défavorable': 'defavorable',
    'réputé favorable par défaut': 'favorable-defaut',
},
}
