# -*- coding: utf-8 -*-
from memo.contenttypes.content.works import IWorks  # NOQA E501
from memo.contenttypes.testing import MEMO_CONTENTTYPES_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
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


class WorksIntegrationTest(unittest.TestCase):

    layer = MEMO_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_works_schema(self):
        fti = queryUtility(IDexterityFTI, name='works')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('works')
        self.assertEqual(schema_name, schema.getName())

    def test_ct_works_fti(self):
        fti = queryUtility(IDexterityFTI, name='works')
        self.assertTrue(fti)

    def test_ct_works_factory(self):
        fti = queryUtility(IDexterityFTI, name='works')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IWorks.providedBy(obj),
            u'IWorks not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_works_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='works',
            id='works',
        )

        self.assertTrue(
            IWorks.providedBy(obj),
            u'IWorks not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('works', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('works', parent.objectIds())

    def test_ct_works_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='works')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_works_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='works')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'works_id',
            title='works container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
