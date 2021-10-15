# -*- coding: utf-8 -*-

from cusy.restapi.patches.interfaces import ICusyRestapiPatchesLayer
from plone.dexterity.interfaces import IDexterityContainer
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer


@implementer(ISerializeToJson)
@adapter(IDexterityContainer, ICusyRestapiPatchesLayer)
class DefaultPageSerializeFolderToJson(SerializeFolderToJson):
    """A custom serializer for default pages for folders.

    Once https://github.com/plone/plone.restapi/pull/944 has been merged,
    this can be removed.
    """

    def __call__(self, version=None, include_items=True):
        result = super(DefaultPageSerializeFolderToJson, self).__call__(
            version=version,
            include_items=include_items,
        )

        if "default_page" in result:
            return result

        default_page = self.context.getDefaultPage()
        if default_page:
            try:
                child = self.context._getOb(default_page)
                serializer = getMultiAdapter((child, self.request), ISerializeToJson)
                default_page_data = serializer()
            except AttributeError:
                print(
                    "Error while generating default page for {0}".format(
                        self.context.absolute_url()
                    )
                )
            else:
                result["default_page"] = default_page_data

        return result
