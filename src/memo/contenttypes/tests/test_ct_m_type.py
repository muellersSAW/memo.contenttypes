# -*- coding: utf-8 -*-
from memo.contenttypes.content.m_type import IMType  # NOQA E501
from memo.contenttypes.testing import MEMO_CONTENTTYPES_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class MTypeIntegrationTest(unittest.TestCase):

    layer = MEMO_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_m_type_schema(self):
        fti = queryUtility(IDexterityFTI, name='MType')
        schema = fti.lookupSchema()
        self.assertEqual(IMType, schema)

    def test_ct_m_type_fti(self):
        fti = queryUtility(IDexterityFTI, name='MType')
        self.assertTrue(fti)

    def test_ct_m_type_factory(self):
        fti = queryUtility(IDexterityFTI, name='MType')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IMType.providedBy(obj),
            u'IMType not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_m_type_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='MType',
            id='m_type',
        )

        self.assertTrue(
            IMType.providedBy(obj),
            u'IMType not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('m_type', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('m_type', parent.objectIds())

    def test_ct_m_type_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='MType')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
