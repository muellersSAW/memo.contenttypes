# -*- coding: utf-8 -*-
from memo.contenttypes.content.authors import IAuthors  # NOQA E501
from memo.contenttypes.testing import MEMO_CONTENTTYPES_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class AuthorsIntegrationTest(unittest.TestCase):

    layer = MEMO_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_authors_schema(self):
        fti = queryUtility(IDexterityFTI, name='authors')
        schema = fti.lookupSchema()
        self.assertEqual(IAuthors, schema)

    def test_ct_authors_fti(self):
        fti = queryUtility(IDexterityFTI, name='authors')
        self.assertTrue(fti)

    def test_ct_authors_factory(self):
        fti = queryUtility(IDexterityFTI, name='authors')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IAuthors.providedBy(obj),
            u'IAuthors not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_authors_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='authors',
            id='authors',
        )

        self.assertTrue(
            IAuthors.providedBy(obj),
            u'IAuthors not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('authors', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('authors', parent.objectIds())

    def test_ct_authors_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='authors')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_authors_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='authors')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'authors_id',
            title='authors container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
