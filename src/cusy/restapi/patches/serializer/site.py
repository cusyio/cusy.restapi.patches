# -*- coding: utf-8 -*-

from cusy.restapi.patches.interfaces import ICusyRestapiPatchesLayer
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.site import SerializeSiteRootToJson
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer


@implementer(ISerializeToJson)
@adapter(IPloneSiteRoot, ICusyRestapiPatchesLayer)
class DefaultPageSerializeSiteRootToJson(SerializeSiteRootToJson):
    """A custom serializer for default pages for the site root.

    Once https://github.com/plone/plone.restapi/pull/944 has been merged,
    this can be removed.
    """

    def __call__(self, version=None):
        result = super(DefaultPageSerializeSiteRootToJson, self).__call__(
            version=version
        )

        if "default_page" in result:
            return result

        default_page = self.context.getDefaultPage()
        if default_page:
            child = self.context._getOb(default_page)
            result["default_page"] = getMultiAdapter(
                (child, self.request), ISerializeToJson
            )()

        return result
