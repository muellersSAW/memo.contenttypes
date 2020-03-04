# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class ICategories(model.Schema):
    """ Marker interface for Categories
    """


@implementer(ICategories)
class Categories(Container):
    """
    """
