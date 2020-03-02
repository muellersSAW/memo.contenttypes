# -*- coding: utf-8 -*-
from memo.contenttypes.testing import MEMO_CONTENTTYPES_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class ManuscriptIntegrationTest(unittest.TestCase):

    layer = MEMO_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_manuscript_schema(self):
        fti = queryUtility(IDexterityFTI, name='manuscript')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('manuscript')
        self.assertEqual(schema_name, schema.getName())

    def test_ct_manuscript_fti(self):
        fti = queryUtility(IDexterityFTI, name='manuscript')
        self.assertTrue(fti)

    def test_ct_manuscript_factory(self):
        fti = queryUtility(IDexterityFTI, name='manuscript')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_manuscript_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='manuscript',
            id='manuscript',
        )


        parent = obj.__parent__
        self.assertIn('manuscript', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('manuscript', parent.objectIds())

    def test_ct_manuscript_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='manuscript')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
