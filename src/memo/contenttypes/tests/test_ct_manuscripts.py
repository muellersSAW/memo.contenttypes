# -*- coding: utf-8 -*-
from memo.contenttypes.content.manuscripts import IManuscripts  # NOQA E501
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


class ManuscriptsIntegrationTest(unittest.TestCase):

    layer = MEMO_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'None',
            self.portal,
            'parent_container',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_manuscripts_schema(self):
        fti = queryUtility(IDexterityFTI, name='manuscripts')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('manuscripts')
        self.assertEqual(schema_name, schema.getName())

    def test_ct_manuscripts_fti(self):
        fti = queryUtility(IDexterityFTI, name='manuscripts')
        self.assertTrue(fti)

    def test_ct_manuscripts_factory(self):
        fti = queryUtility(IDexterityFTI, name='manuscripts')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IManuscripts.providedBy(obj),
            u'IManuscripts not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_manuscripts_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='manuscripts',
            id='manuscripts',
        )

        self.assertTrue(
            IManuscripts.providedBy(obj),
            u'IManuscripts not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('manuscripts', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('manuscripts', parent.objectIds())

    def test_ct_manuscripts_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='manuscripts')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_manuscripts_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='manuscripts')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'manuscripts_id',
            title='manuscripts container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
