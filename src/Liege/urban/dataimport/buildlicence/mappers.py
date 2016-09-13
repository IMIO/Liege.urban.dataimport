# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.mapper import AccessFinalMapper as FinalMapper
from imio.urban.dataimport.access.mapper import AccessMapper as Mapper
from imio.urban.dataimport.access.mapper import AccessPostCreationMapper as PostCreationMapper
from imio.urban.dataimport.access.mapper import SubQueryMapper

from imio.urban.dataimport.exceptions import NoObjectToCreateException

from imio.urban.dataimport.factory import BaseFactory

from plone import api


#
# LICENCE
#

# factory


class LicenceFactory(BaseFactory):
    def getCreationPlace(self, factory_args):
        path = '%s/urban/buildlicences' % self.site.absolute_url_path()
        return self.site.restrictedTraverse(path)

# mappers


class ReferenceMapper(PostCreationMapper):
    def mapReference(self, line, plone_object):
        shore_abbr = {
            'right': u'D',
            'left': u'G',
            'center': u'C',
        }
        shore = shore_abbr.get(plone_object.shore, '')

        ref = 'PU/{} {}'.format(self.getData('NUMDOSSIERBKP'), shore)
        return ref


class TypeAndCategoryMapper(Mapper):
    """ """
    def mapPortal_type(self, line):
        type_value = self.getData('NORM_UNIK').upper()
        portal_type = self.getValueMapping('type_map')[type_value]['portal_type']
        if not portal_type:
            self.logError(self, line, 'No portal type found for this type value', {'TYPE value': type_value})
            raise NoObjectToCreateException
        return portal_type

    def mapFoldercategory(self, line):
        type_value = self.getData('NORM_UNIK').upper()
        foldercategory = self.getValueMapping('type_map')[type_value]['foldercategory']
        return foldercategory


class FolderCategoryMapper(Mapper):
    """ """
    def mapFoldercategorytownship(self, line):
        return self.getData('CODE NAT TRAVAUX')


class CompletionStateMapper(PostCreationMapper):
    def map(self, line, plone_object):
        self.line = line
        workflow_tool = api.portal.get_tool('portal_workflow')
        raw_state = self.getData('COLLDECISION').lower()
        if 'sans' in raw_state and 'suite' in raw_state:
            raw_state = 'sans suite'
        state_mapping = self.getValueMapping('state_map')
        state = state_mapping.get(raw_state, '')

        workflow_def = workflow_tool.getWorkflowsFor(plone_object)[0]
        workflow_id = workflow_def.getId()
        workflow_state = workflow_tool.getStatusOf(workflow_id, plone_object)
        workflow_state['review_state'] = state
        workflow_tool.setStatusOf(workflow_id, plone_object, workflow_state.copy())


class ErrorsMapper(FinalMapper):
    def mapDescription(self, line, plone_object):

        line_number = self.importer.current_line
        errors = self.importer.errors.get(line_number, None)
        description = plone_object.Description()

        error_trace = []

        if errors:
            for error in errors:
                data = error.data
                if 'streets' in error.message:
                    error_trace.append('<p>adresse : %s</p>' % data['address'])
                elif 'notaries' in error.message:
                    error_trace.append('<p>notaire : %s %s %s</p>' % (data['title'], data['firstname'], data['name']))
                elif 'architects' in error.message:
                    error_trace.append('<p>architecte : %s</p>' % data['raw_name'])
                elif 'geometricians' in error.message:
                    error_trace.append('<p>géomètre : %s</p>' % data['raw_name'])
                elif 'parcelling' in error.message:
                    error_trace.append('<p>lotissement : %s %s, autorisé le %s</p>' % (data['approval date'], data['city'], data['auth_date']))
                elif 'article' in error.message.lower():
                    error_trace.append('<p>Articles de l\'enquête : %s</p>' % (data['articles']))
        error_trace = ''.join(error_trace)

        return '%s%s' % (error_trace, description)
