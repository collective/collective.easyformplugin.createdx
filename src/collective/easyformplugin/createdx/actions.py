from collective.easyform.actions import Action
from collective.easyform.actions import ActionFactory
from collective.easyform.api import get_context
from collective.easyform.api import get_schema
from collective.easyform.api import OrderedDict
from collective.easyformplugin.createdx.interfaces import ICreateDX
from zope.interface import implementer
from collective.easyform.api import get_schema
from collective.easyform.interfaces.savedata import ISaveData
from plone.supermodel.exportimport import BaseHandler
from collective.easyformplugin.createdx import _


@implementer(ICreateDX)
class CreateDX(Action):
    """  """

    def __init__(self, **kw):
        for i, f in ICreateDX.namesAndDescriptions():
            setattr(self, i, kw.pop(i, f.default))
        super(CreateDX, self).__init__(**kw)


    def createDXItem(self, fields, request, context):
      """
      """


    def onSuccess(self, fields, request):
        """
        e-mails data.
        """
        context = get_context(self)
        mailtext = self.get_mail_text(fields, request, context)
        host = context.MailHost
        host.send(mailtext)


CreateDXAction = ActionFactory(
    CreateDX,
    _(u'label_create_dexterity_content', default=u'Create dexterity content'),
    'collective.easyform.AddDXContent',
)

CreateDXHandler = BaseHandler(CreateDX)
