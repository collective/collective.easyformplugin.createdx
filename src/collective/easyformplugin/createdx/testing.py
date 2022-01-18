# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.easyformplugin.createdx


class CollectiveEasyformpluginCreatedxLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.easyformplugin.createdx)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.easyformplugin.createdx:default")


COLLECTIVE_EASYFORMPLUGIN_CREATEDX_FIXTURE = CollectiveEasyformpluginCreatedxLayer()


COLLECTIVE_EASYFORMPLUGIN_CREATEDX_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_EASYFORMPLUGIN_CREATEDX_FIXTURE,),
    name="CollectiveEasyformpluginCreatedxLayer:IntegrationTesting",
)


COLLECTIVE_EASYFORMPLUGIN_CREATEDX_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_EASYFORMPLUGIN_CREATEDX_FIXTURE,),
    name="CollectiveEasyformpluginCreatedxLayer:FunctionalTesting",
)


COLLECTIVE_EASYFORMPLUGIN_CREATEDX_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_EASYFORMPLUGIN_CREATEDX_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveEasyformpluginCreatedxLayer:AcceptanceTesting",
)
