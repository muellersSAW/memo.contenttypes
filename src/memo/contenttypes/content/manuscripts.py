# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IManuscripts(model.Schema):
    """ Marker interface for Manuscripts
    """


@implementer(IManuscripts)
class Manuscripts(Container):
    """
    """
