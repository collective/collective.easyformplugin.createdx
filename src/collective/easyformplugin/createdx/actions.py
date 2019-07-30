# -*- coding: utf-8 -*-
from collective.easyform.actions import Action
from collective.easyform.actions import ActionFactory
from collective.easyform.api import get_context
from collective.easyformplugin.createdx import _
from collective.easyformplugin.createdx.interfaces import ICreateDX
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.supermodel.exportimport import BaseHandler
from zope.container.interfaces import INameChooser
from zope.interface import implementer

import pytz


def intellitext_converter(value):
    """convert plain text to html
    """
    portal_transforms = api.portal.get_tool(name='portal_transforms')
    stream = portal_transforms.convertTo(
        'text/html', value, mimetype='text/x-web-intelligent',
    )
    return RichTextValue(
        raw=stream.getData().strip(),
        mimeType='text/html',
        outputMimeType='text/x-html-safe',
        encoding='utf-8',
    )


def add_timezone_converter(value):
    """Add localized timezone to be able to use value as event start
    """
    portal_timezone = api.portal.get_registry_record('plone.portal_timezone')
    tz = pytz.timezone(portal_timezone)
    return tz.localize(value)


CONVERT_MAP = {
    'plaintext_to_intellitext': intellitext_converter,
    'datetime_with_timezone': add_timezone_converter,
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

        location = api.content.get(
            path=self.location.encode('ascii', 'ignore'),
        )

        if 'id' in mappings and mappings['id']:
            title_or_id = mappings['id']
        else:
            title_or_id = mappings['title']

        chooser = INameChooser(location)
        item_id = chooser.chooseName(title_or_id, location)

        api.content.create(
            container=location,
            type=self.content_type,
            id=item_id,
            **mappings  # noqa C815
        )

    def onSuccess(self, fields, request):
        """Create item on successful form submission
        """
        context = get_context(self)
        current_user = api.user.get_current()

        with api.env.adopt_user(user=current_user):
            with api.env.adopt_roles(roles=['Contributor']):
                self.createDXItem(fields, request, context)


CreateDXAction = ActionFactory(
    CreateDX,
    _(u'label_create_dexterity_content', default=u'Create dexterity content'),
    'collective.easyform.AddDXContent',
)

CreateDXHandler = BaseHandler(CreateDX)
