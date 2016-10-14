# -*- coding: utf-8 -*-

from imio.urban.dataimport.mapping import table

VALUES_MAPS = {

'type_map': table({
'header'  : ['portal_type',  'foldercategory', 'abreviation'],
'N'       : ['BuildLicence', 'pn',             'PU'],
'U'       : ['BuildLicence', 'pu',             'U'],
'M'       : ['',   '',               '127'],  # Article127
'I'       : ['BuildLicence', 'pi',             'PI'],
'V'       : ['',   '',               'V'],  # Article127
'D'       : ['',  '',               'D'],  # Declaration
''        : ['',             '',               ''],
}),

'state_map': {
    'autorisé': 'accepted',
    'recevable': 'accepted',
    'refusé': 'refused',
    'refusé tacite': 'refused',
    'refusé par défaut': 'refused',
    'irrecevable': 'refused',
    'sans suite': 'field_away',
    'abandonné': 'abandoned',
},

'eventtype_id_map': table({
    'header'             : ['decision_event',                       'deposit_event',       'second_deposit_event'],
    'BuildLicence'       : ['delivrance-du-permis-octroi-ou-refus', 'depot-de-la-demande', 'recepisse-art15-complement'],
    'Article127'         : ['delivrance-du-permis-octroi-ou-refus', 'depot-de-la-demande', 'recepisse-art15-complement'],
    'Declaration'        : ['deliberation-college',                 'depot-de-la-demande', 'depot-de-la-demande'],
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
