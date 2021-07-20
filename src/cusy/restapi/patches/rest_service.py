# -*- coding: utf-8 -*-

from plone.app.layout.navigation.root import getNavigationRootObject
from zope.component.hooks import setSite
from zope.interface.interfaces import ComponentLookupError

import plone.api


def __call__(self):
    """Set the site so all utility lookups take the correct context."""
    portal = plone.api.portal.get()
    navigation_root = getNavigationRootObject(self.context, portal)
    try:
        setSite(navigation_root)
    except ComponentLookupError:
        setSite(portal)

    return self._old_cusy_restapi_patches___call__()


def customPatchHandler(scope, original, replacement):  # noqa: N802
    """Custom handler that preserves original method with a custom name."""
    OLD_NAME = "_old_cusy_restapi_patches_{0}".format(original)  # noqa: N806

    if not getattr(scope, OLD_NAME, None):
        setattr(scope, OLD_NAME, getattr(scope, original))

    setattr(scope, original, replacement)
    return
