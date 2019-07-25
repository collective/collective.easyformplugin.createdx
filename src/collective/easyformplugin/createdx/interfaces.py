# -*- coding: utf-8 -*-
import zope.schema.interfaces
import zope.interface
import zope.i18nmessageid
from z3c.form.browser.textarea import TextAreaWidget
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.supermodel.model import fieldset
from plone.schema import Email
from plone.autoform import directives
from plone.app.textfield import RichText
from collective.easyform.interfaces import IAction
from collective.easyform import config
from collective.easyform.actions import IAction
from collective.easyform import vocabularies
from collective.easyformplugin.createdx import _
from plone import schema


class ICreateDX(IAction):

    """
    """
