# -*- coding: utf-8 -*-
from site import execsitecustomize
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
from plone.namedfile.file import NamedBlobFile

import logging
import pytz


logger = logging.getLogger(__name__)


def intellitext_converter(value):
    """convert plain text to html"""
    portal_transforms = api.portal.get_tool(name="portal_transforms")
    stream = portal_transforms.convertTo(
        "text/html",
        value,
        mimetype="text/x-web-intelligent",
    )
    return RichTextValue(
        raw=stream.getData().strip(),
        mimeType="text/html",
        outputMimeType="text/x-html-safe",
        encoding="utf-8",
    )


def add_timezone_converter(value):
    """Add localized timezone to be able to use value as event start"""
    portal_timezone = api.portal.get_registry_record("plone.portal_timezone")
    tz = pytz.timezone(portal_timezone)
    return tz.localize(value)

def fileupload_to_namedblobfile_converter(value):
    breakpoint()
    return NamedBlobFile(value.data, filename=value.filename)


CONVERT_MAP = {
    "plaintext_to_intellitext": intellitext_converter,
    "datetime_with_timezone": add_timezone_converter,
    "fileupload_converter": fileupload_to_namedblobfile_converter,
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
        """Create dexterity item and call converters as necessary"""
        mappings = {}
        for mapping in self.mappings:
            try:
                src_field, target_def = mapping.split(" ")
            except ValueError:
                logger.exception(f"Configuration of mapping wrong: {mapping} (ignored)")
                continue
            if src_field not in fields:
                logger.error(f"Undefined field {src_field} configured!")
                continue
            if ":" not in target_def:
                target_def += ":"
            target_field, field_type = target_def.split(":")
            mappings[target_field] = self.convert_field(
                field_type,
                fields[src_field],
            )

        if "id" in mappings and mappings["id"]:
            title_or_id = mappings["id"]
        elif "title" in mappings and mappings["title"]:
            title_or_id = mappings["title"]
        else:
            raise ValueError("Neither id nor title mapped.")

        location = api.content.get(path=self.location)
        if not location:
            raise ValueError(f"Target location can not be found: {self.location}")

        chooser = INameChooser(location)
        item_id = chooser.chooseName(title_or_id, location)

        api.content.create(
            container=location,
            type=self.content_type,
            id=item_id,
            **mappings  # noqa C815
        )

    def onSuccess(self, fields, request):
        """Create item on successful form submission"""
        context = get_context(self)
        current_user = api.user.get_current()

        with api.env.adopt_user(user=current_user):
            with api.env.adopt_roles(roles=["Contributor"]):
                self.createDXItem(fields, request, context)


CreateDXAction = ActionFactory(
    CreateDX,
    _(u"label_create_dexterity_content", default=u"Create dexterity content"),
    "collective.easyform.AddDXContent",
)

CreateDXHandler = BaseHandler(CreateDX)
