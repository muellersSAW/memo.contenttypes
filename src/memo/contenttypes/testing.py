# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import memo.contenttypes


class MemoContenttypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=memo.contenttypes)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'memo.contenttypes:default')


MEMO_CONTENTTYPES_FIXTURE = MemoContenttypesLayer()


MEMO_CONTENTTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEMO_CONTENTTYPES_FIXTURE,),
    name='MemoContenttypesLayer:IntegrationTesting',
)


MEMO_CONTENTTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MEMO_CONTENTTYPES_FIXTURE,),
    name='MemoContenttypesLayer:FunctionalTesting',
)


MEMO_CONTENTTYPES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        MEMO_CONTENTTYPES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='MemoContenttypesLayer:AcceptanceTesting',
)
