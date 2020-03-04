# -*- coding: utf-8 -*-
from memo.contenttypes.content.categories import ICategories  # NOQA E501
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


class CategoriesIntegrationTest(unittest.TestCase):

    layer = MEMO_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_categories_schema(self):
        fti = queryUtility(IDexterityFTI, name='categories')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('categories')
        self.assertEqual(schema_name, schema.getName())

    def test_ct_categories_fti(self):
        fti = queryUtility(IDexterityFTI, name='categories')
        self.assertTrue(fti)

    def test_ct_categories_factory(self):
        fti = queryUtility(IDexterityFTI, name='categories')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ICategories.providedBy(obj),
            u'ICategories not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_categories_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='categories',
            id='categories',
        )

        self.assertTrue(
            ICategories.providedBy(obj),
            u'ICategories not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('categories', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('categories', parent.objectIds())

    def test_ct_categories_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='categories')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_categories_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='categories')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'categories_id',
            title='categories container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
