# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IWorks(model.Schema):
    """ Marker interface for Works
    """


@implementer(IWorks)
class Works(Container):
    """
    """
