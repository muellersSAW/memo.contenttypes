# -*- coding: utf-8 -*-
from memo.contenttypes.content.language import ILanguage  # NOQA E501
from memo.contenttypes.testing import MEMO_CONTENTTYPES_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class LanguageIntegrationTest(unittest.TestCase):

    layer = MEMO_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_language_schema(self):
        fti = queryUtility(IDexterityFTI, name='Language')
        schema = fti.lookupSchema()
        self.assertEqual(ILanguage, schema)

    def test_ct_language_fti(self):
        fti = queryUtility(IDexterityFTI, name='Language')
        self.assertTrue(fti)

    def test_ct_language_factory(self):
        fti = queryUtility(IDexterityFTI, name='Language')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ILanguage.providedBy(obj),
            u'ILanguage not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_language_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Language',
            id='language',
        )

        self.assertTrue(
            ILanguage.providedBy(obj),
            u'ILanguage not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('language', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('language', parent.objectIds())

    def test_ct_language_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Language')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
