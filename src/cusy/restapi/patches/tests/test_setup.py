# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from cusy.restapi.patches.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that cusy.restapi.patches is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if cusy.restapi.patches is installed."""
        self.assertTrue(self.installer.is_product_installed("cusy.restapi.patches"))

    def test_browserlayer(self):
        """Test that ICusyRestapiPatchesLayer is registered."""
        from cusy.restapi.patches.interfaces import ICusyRestapiPatchesLayer
        from plone.browserlayer import utils

        self.assertIn(ICusyRestapiPatchesLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("cusy.restapi.patches")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if cusy.restapi.patches is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("cusy.restapi.patches"))

    def test_browserlayer_removed(self):
        """Test that ICusyRestapiPatchesLayer is removed."""
        from cusy.restapi.patches.interfaces import ICusyRestapiPatchesLayer
        from plone.browserlayer import utils

        self.assertNotIn(ICusyRestapiPatchesLayer, utils.registered_layers())
