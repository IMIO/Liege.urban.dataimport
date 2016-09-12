# -*- coding: utf-8 -*-

from imio.urban.dataimport.access.mapper import AccessFinalMapper as FinalMapper
from imio.urban.dataimport.access.mapper import AccessMapper as Mapper
from imio.urban.dataimport.access.mapper import AccessPostCreationMapper as PostCreationMapper
from imio.urban.dataimport.access.mapper import SubQueryMapper

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


class PortalTypeMapper(Mapper):
    def mapPortal_type(self, line):
        return 'BuildLicence'


class ReferenceMapper(PostCreationMapper):
    def mapReference(self, line, plone_object):
        shore_abbr = {
            'right': u'D',
            'left': u'G',
            'center': u'C',
        }
        shore = shore_abbr[plone_object.shore]

        ref = 'PU/{} {}'.format(self.getData('NUMERO DE DOSSIER'), shore)
        return ref


class CategoryMapper(Mapper):
    """ """


class WorkTypeMapper(Mapper):
    def mapWorktype(self, line):
        worktype = self.getData('Code_220+')
        return [worktype]


class CompletionStateMapper(PostCreationMapper):
    def map(self, line, plone_object):
        self.line = line
        state = ''
        if self.getData('Autorisa') or self.getData('TutAutorisa'):
            state = 'accepted'
        elif self.getData('Refus') or self.getData('TutRefus'):
            state = 'refused'
        else:
            return
        workflow_tool = api.portal.get_tool('portal_workflow')
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
