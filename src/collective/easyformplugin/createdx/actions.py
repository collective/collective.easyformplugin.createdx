# -*- coding: utf-8 -*-
from collective.easyform.actions import Action
from collective.easyform.actions import ActionFactory
from collective.easyform.api import get_context
from collective.easyformplugin.createdx import _
from collective.easyformplugin.createdx.interfaces import ICreateDX
from plone import api
from plone.supermodel.exportimport import BaseHandler
from zope.interface import implementer

import pytz

# def richtext_handler(value):
#     value = ... convert here
#     return value


# def textline_handler(value):
#     value = ... convert here
#     return value


def datetime_handler(value):
    """Add localized timezone to be able to use value as event start
    """
    portal_timezone = api.portal.get_registry_record('plone.portal_timezone')
    tz = pytz.timezone(portal_timezone)
    # value = ... convert here
    return tz.localize(value)


CONVERT_MAP = {
#     'richtext': richtext_handler,
#     'textline': textline_handler,
    'datetime': datetime_handler,
}



@implementer(ICreateDX)
class CreateDX(Action):
    """Create Dexterity Item Action"""

    def __init__(self, **kw):
        for i, f in ICreateDX.namesAndDescriptions():
            setattr(self, i, kw.pop(i, f.default))
        super(CreateDX, self).__init__(**kw)

    def convert_field(self, field_type, value):
        converter = CONVERT_MAP.get(field_type, None)
        if converter is None:
                return value
        return converter(value)


    def createDXItem(self, fields, request, context):
        """Create dexterity item and call converters as necessary
        """
        mappings = {}
        for m in self.mappings:
            src_field, v = m.split(' ')
            if ':' not in v:
                v += ':'
            target_field, field_type = v.split(':')
            mappings[target_field] = self.convert_field(
                field_type,
                fields[src_field],
            )

        api.content.create(
            container=api.content.get(path='/foam/entries'),
            type=self.content_type,
            # title=fields['topic'],
            # text=fields['comments']
            **mappings
        )


    def onSuccess(self, fields, request):
        """Create item on successful form submission
        """
        context = get_context(self)
        self.createDXItem(fields, request, context)


CreateDXAction = ActionFactory(
    CreateDX,
    _(u'label_create_dexterity_content', default=u'Create dexterity content'),
    'collective.easyform.AddDXContent',
)

CreateDXHandler = BaseHandler(CreateDX)
