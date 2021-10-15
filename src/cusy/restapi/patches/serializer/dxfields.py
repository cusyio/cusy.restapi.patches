# -*- coding: utf-8 -*-

from cusy.restapi.patches.interfaces import ICusyRestapiPatchesLayer
from plone.app.contenttypes.interfaces import ILink
from plone.app.contenttypes.utils import replace_link_variables_by_paths
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxfields import TextLineFieldSerializer
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.schema.interfaces import ITextLine


try:
    from plone.restapi.serializer.utils import uid_to_url
except ImportError:
    uid_to_url = None


@adapter(ITextLine, ILink, ICusyRestapiPatchesLayer)
class PatchedTextLineFieldSerializer(TextLineFieldSerializer):
    def __call__(self):
        if self.field.getName() != "remoteUrl":
            return super(PatchedTextLineFieldSerializer, self).__call__()
        value = self.get_value()

        # Remove all leading slashes
        while value.startswith("/") and len(value) > 0:
            value = value[1:]

        # Expect that all internal links will have resolveuid
        if uid_to_url and callable(uid_to_url) and value and "resolveuid" in value:
            return uid_to_url(value)

        # Fallback in case we still have a variable in there
        path = replace_link_variables_by_paths(context=self.context, url=value)
        portal = getMultiAdapter(
            (self.context, self.context.REQUEST), name="plone_portal_state"
        ).portal()
        # We should traverse unrestricted, just in case that the path to the object
        # is not all public, we should be able to reach it by finger pointing
        ref_obj = portal.restrictedTraverse(path, None)
        if ref_obj:
            try:
                value = ref_obj.absolute_url()
            except AttributeError:
                value = path
                name = getattr(ref_obj.__class__, "__name__", "")
                if name.startswith("SimpleViewClass"):
                    context_path = "/".join(ref_obj.context.getPhysicalPath())
                    link_path = path.replace(context_path, "")
                    # Remove leading slash
                    if link_path.startswith("/"):
                        link_path = link_path[1:]
                    value = "/".join([ref_obj.context.absolute_url(), link_path])
            return json_compatible(value)
        else:
            # The URL does not point to an existing object, so just return the path
            return json_compatible(path)
