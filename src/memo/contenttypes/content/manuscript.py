# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
# from zope import schema
from plone import api
from zope.interface import implementer
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from memo.contenttypes.content.library import ILibrary
from memo.contenttypes import _


def basePath(context=None):
  uid = api.portal.get_registry_record('uid_of_configurable_folder', default = None)
  if not uid:
    # Root Portal Path
    folder = api.portal.get()
  else:
    # Folder Start Path
    folder = api.content.get(UID=uid)
  return '/'.join(folder.getPhysicalPath())

class IManuscript(model.Schema):
    """ Marker interface and Dexterity Python Schema for Manuscript
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    model.load('manuscript.xml')


    directives.widget(
            "library",
            RelatedItemsFieldWidget,
            pattern_options={'basePath': '/',
                'folderTypes': ['libraries'],
                "mode": "auto",
                "favorites": []},
    )

    library = RelationChoice(
        title=_(u"Library"),
        # source=ObjPathSourceBinder(object_provides=ILibrary.__identifier__),
        source=CatalogSource(portal_type=['Library']),
        required=False,
    )


    related_obj = RelationChoice(
    title=_(u"Referenziertes Objekt"),
    source=ObjPathSourceBinder(
        portal_type="MyRelatedObjType",
        navigation_tree_query=dict(
            portal_type=["MyRelatedObjType",],
            path={ "query": '/ub/ub-db' })
    ),
    required=False,
)


    # directives.widget(level=RadioFieldWidget)
    # level = schema.Choice(
    #     title=_(u'Sponsoring Level'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    # history = RichText(
    #     title=_(u'History'),
    #     required=False
    # )

    # url = schema.URI(
    #     title=_(u'Link'),
    #     required=False
    # )

    # fieldset('Images', fields=['logo', 'advertisement'])
    # logo = namedfile.NamedBlobImage(
    #     title=_(u'Logo'),
    #     required=False,
    # )

    # advertisement = namedfile.NamedBlobImage(
    #     title=_(u'Advertisement (Gold-sponsors and above)'),
    #     required=False,
    # )

    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # notes = RichText(
    #     title=_(u'Secret Notes (only for site-admins)'),
    #     required=False
    # )


@implementer(IManuscript)
class Manuscript(Item):
    """
    """
