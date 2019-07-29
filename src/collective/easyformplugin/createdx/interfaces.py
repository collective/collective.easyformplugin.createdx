# -*- coding: utf-8 -*-
from collective.easyform.interfaces import IAction
from z3c.relationfield.schema import RelationChoice
from collective.easyformplugin.createdx import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone import schema
from plone.app.z3cform.widget import SelectFieldWidget
from zope.interface import Interface
from z3c.form.browser.textlines import TextLinesFieldWidget


class ICreateDX(IAction):
    """Create a Dexterity Type"""

    location = schema.TextLine(
        title=_(u'Location'),
        description=_(
            u'Select the location where content items should be created'),
        required=True,
    )

    content_type = schema.Choice(
        title=_(u'label_content_type', default=u'Content Type'),
        vocabulary='plone.app.vocabularies.PortalTypes',
        required=True,
        default='',
        missing_value='',
    )
    directives.widget('content_type', SelectFieldWidget)

    mappings = schema.List(
        title=_(u'Form field to item field mappings'),
        description=_(
            u'One mapping per line. Format: "formfieldid itemfieldid:fieldtype"'),
        default=[],
        required=False,
        value_type=schema.TextLine(),
    )

    directives.widget('mappings', TextLinesFieldWidget)
