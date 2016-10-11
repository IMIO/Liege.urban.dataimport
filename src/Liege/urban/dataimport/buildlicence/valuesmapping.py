# -*- coding: utf-8 -*-

from imio.urban.dataimport.mapping import table

VALUES_MAPS = {

'type_map': table({
'header'  : ['portal_type',  'foldercategory', 'abreviation'],
'N'       : ['BuildLicence', 'pn',             'PU'],
'U'       : ['BuildLicence', 'pu',             'U'],
'M'       : ['Article127',   '',               '127'],
'I'       : ['BuildLicence', 'pi',             'PI'],
'V'       : ['Article127',   '',               'V'],
'D'       : ['',             '',               'D'],
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
    'header'             : ['decision_event'],
    'BuildLicence'       : ['delivrance-du-permis-octroi-ou-refus'],
    'ParcelOutLicence'   : ['delivrance-du-permis-octroi-ou-refus'],
    'Declaration'        : ['deliberation-college'],
    'UrbanCertificateOne': ['octroi-cu1'],
    'UrbanCertificateTwo': ['octroi-cu2'],
    'MiscDemand'         : ['deliberation-college'],
    'EnvClassOne'        : ['decision'],
    'EnvClassTwo'        : ['desision'],
    'EnvClassThree'      : ['acceptation-de-la-demande'],
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
