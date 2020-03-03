# -*- coding: utf-8 -*-
from memo.contenttypes.content.category import ICategory  # NOQA E501
from memo.contenttypes.testing import MEMO_CONTENTTYPES_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class CategoryIntegrationTest(unittest.TestCase):

    layer = MEMO_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_category_schema(self):
        fti = queryUtility(IDexterityFTI, name='Category')
        schema = fti.lookupSchema()
        self.assertEqual(ICategory, schema)

    def test_ct_category_fti(self):
        fti = queryUtility(IDexterityFTI, name='Category')
        self.assertTrue(fti)

    def test_ct_category_factory(self):
        fti = queryUtility(IDexterityFTI, name='Category')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ICategory.providedBy(obj),
            u'ICategory not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_category_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Category',
            id='category',
        )

        self.assertTrue(
            ICategory.providedBy(obj),
            u'ICategory not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('category', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('category', parent.objectIds())

    def test_ct_category_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Category')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
