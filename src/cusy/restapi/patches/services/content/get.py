# -*- coding: utf-8 -*-

from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from Products.CMFDynamicViewFTI.interfaces import ISelectableBrowserDefault
from zope.component import queryMultiAdapter


class ContentGet(Service):
    """Returns a serialized content object."""

    def reply(self):
        """Patched version of the conent sercice.

        Once https://github.com/plone/plone.restapi/pull/944 has been merged,
        this can be removed.
        """
        serializer = None
        if ISelectableBrowserDefault.providedBy(self.context):
            if not self.context.getDefaultPage():
                layout = self.context.getLayout()
                serializer = queryMultiAdapter(
                    (self.context, self.request), ISerializeToJson, name=layout
                )

        if serializer is None:
            serializer = queryMultiAdapter(
                (self.context, self.request), ISerializeToJson
            )

        if serializer is None:
            self.request.response.setStatus(501)
            return dict(error=dict(message="No serializer available."))

        return serializer(version=self.request.get("version"))
