# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import cusy.restapi.patches


class CusyRestapiPatchesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=cusy.restapi.patches)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cusy.restapi.patches:default')


CUSY_RESTAPI_PATCHES_FIXTURE = CusyRestapiPatchesLayer()


CUSY_RESTAPI_PATCHES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CUSY_RESTAPI_PATCHES_FIXTURE,),
    name='CusyRestapiPatchesLayer:IntegrationTesting',
)


CUSY_RESTAPI_PATCHES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CUSY_RESTAPI_PATCHES_FIXTURE,),
    name='CusyRestapiPatchesLayer:FunctionalTesting',
)


CUSY_RESTAPI_PATCHES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CUSY_RESTAPI_PATCHES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CusyRestapiPatchesLayer:AcceptanceTesting',
)
