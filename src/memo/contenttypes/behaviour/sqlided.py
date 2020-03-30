from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.interface import provider

@provider(IFormFieldProvider)
class IIded(model.Schema):

    directives.fieldset(
        'ided',
        label=u'sql id',
        fields=('sqlid',),
    )

    sqlid = schema.Int(
        title=u'This is the old sql id, needed for import',
        required=False,
    )
