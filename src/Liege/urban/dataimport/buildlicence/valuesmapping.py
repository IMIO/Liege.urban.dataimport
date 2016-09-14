# -*- coding: utf-8 -*-

from imio.urban.dataimport.mapping import table

VALUES_MAPS = {

'type_map': table({
'header'  : ['portal_type',  'foldercategory', 'abreviation'],
'N'       : ['BuildLicence', 'pn',             'PU'],
'U'       : ['BuildLicence', 'pu',             'U'],
'M'       : ['',             '',               '127'],
'I'       : ['BuildLicence', 'pi',             'PI'],
'V'       : ['',             '',               'V'],
'D'       : ['',             '',               'D'],
}),

'state_map': {
    'autorisé': 'accepted',
    'refusé': 'refused',
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

'documents_map': {
    'BuildLicence': 'URBA',
    'UniqueLicence': 'PERMIS-UNIQUE',
    'ParcelOutLicence': 'LOTISSEMENT',
    'Declaration': 'REGISTRE-PU',
    'UrbanCertificateOne': 'CU/1',
    'UrbanCertificateTwo': 'CU/2',
    'MiscDemand': 'AUTRE DOSSIER',
    'EnvClassOne': 'ENVIRONNEMENT',
    'EnvClassTwo': 'ENVIRONNEMENT',
    'EnvClassThree': 'ENVIRONNEMENT',
},

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
    'mademoiselle': 'miss',
    'melle': 'miss',
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
    'F': 'favorable',
    'FC': 'favorable-conditionnel',
    'D': 'defavorable',
    'RF': 'favorable-defaut',
},
}
