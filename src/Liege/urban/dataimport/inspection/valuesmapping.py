# -*- coding: utf-8 -*-

from imio.urban.dataimport.mapping import table

VALUES_MAPS = {

'type_map': table({
'header'  : ['portal_type',          'abreviation'],
'AP'      : ['PreliminaryNotice',    'AP'],
'CU'      : ['UrbanCertificateOne',  'CU1'],
'PAT'     : ['PatrimonyCertificate', 'PAT'],
'DUP'     : ['Declaration',          'D'],
'ADEM'    : ['',                     ''],
'AMEN'    : ['',                     ''],
'AT'      : ['',                     ''],
'DEM'     : ['',                     ''],
'DIV'     : ['',                     ''],
'DIM'     : ['',                     ''],
'PAP'     : ['',                     ''],
'TER'     : ['',                     ''],
}),

'state_map': {
    'Favorable': 'accepted',
    'Défavorable': 'refused',
},

'eventtype_id_map': table({
    'header'               : ['decision_event',       'deposit_event'],
    'UrbanCertificateTwo'  : ['copy_of_octroi-cu2',   'depot-de-la-demande'],
    'UrbanCertificateOne'  : ['',                     'copy_of_depot-de-la-demande'],
    'PreliminaryNotice'    : ['',                     'copy_of_depot-de-la-demande'],
    'Declaration'          : ['',                     'depot-de-la-demande'],
    'PatrimonyCertificate' : ['',                     'convocation'],
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
