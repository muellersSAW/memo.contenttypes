# -*- coding: utf-8 -*-
from memo.contenttypes.content.library import ILibrary  # NOQA E501
from memo.contenttypes.testing import MEMO_CONTENTTYPES_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class LibraryIntegrationTest(unittest.TestCase):

    layer = MEMO_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_library_schema(self):
        fti = queryUtility(IDexterityFTI, name='Library')
        schema = fti.lookupSchema()
        self.assertEqual(ILibrary, schema)

    def test_ct_library_fti(self):
        fti = queryUtility(IDexterityFTI, name='Library')
        self.assertTrue(fti)

    def test_ct_library_factory(self):
        fti = queryUtility(IDexterityFTI, name='Library')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ILibrary.providedBy(obj),
            u'ILibrary not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_library_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Library',
            id='library',
        )

        self.assertTrue(
            ILibrary.providedBy(obj),
            u'ILibrary not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('library', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('library', parent.objectIds())

    def test_ct_library_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Library')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
