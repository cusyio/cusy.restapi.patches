# -*- coding: utf-8 -*-

from collections import defaultdict
from cusy.restapi.patches.interfaces import ICusyRestapiPatchesLayer
from plone.memoize.view import memoize
from plone.registry.interfaces import IRegistry
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from plone.restapi.services.navigation.get import Navigation
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from zope.component import adapter, getUtility
from zope.i18n import translate
from zope.interface import implementer, Interface


@implementer(IExpandableElement)
@adapter(Interface, ICusyRestapiPatchesLayer)
class CusyNavigation(Navigation):
    @property
    @memoize
    def navtree(self):
        """Patched version of the navigation serice.

        Once https://github.com/plone/plone.restapi/issues/1107 is fixed, this can be
        removed.
        """
        ret = defaultdict(list)
        navtree_path = self.navtree_path
        for tab in self.portal_tabs:
            entry = {}
            entry.update(
                {
                    "path": "/".join((navtree_path, tab["id"])),
                    "description": tab["description"],
                    "@id": tab["url"],
                }
            )
            if "review_state" in tab:
                entry["review_state"] = json_compatible(tab["review_state"])
            else:
                entry["review_state"] = None

            if "title" not in entry:
                entry["title"] = tab.get("name") or tab.get("description") or tab["id"]
            else:
                # translate Home tab
                entry["title"] = translate(
                    entry["title"], domain="plone", context=self.request
                )

            entry["title"] = safe_unicode(entry["title"])
            ret[navtree_path].append(entry)

        query = {
            "path": {
                "query": self.navtree_path,
                "depth": self.depth,
            },
            "portal_type": {"query": self.settings["displayed_types"]},
            "Language": self.current_language,
            "is_default_page": False,
            # Added to get correct sort order.
            "sort_on": "getObjPositionInParent",
        }

        if not self.settings["nonfolderish_tabs"]:
            query["is_folderish"] = True

        if self.settings["filter_on_workflow"]:
            query["review_state"] = list(self.settings["workflow_states_to_show"] or ())

        if not self.settings["show_excluded_items"]:
            query["exclude_from_nav"] = False

        context_path = "/".join(self.context.getPhysicalPath())
        portal_catalog = getToolByName(self.context, "portal_catalog")
        brains = portal_catalog.searchResults(**query)

        registry = getUtility(IRegistry)
        types_using_view = registry.get("plone.types_use_view_action_in_listings", [])

        for brain in brains:
            brain_path = brain.getPath()
            brain_parent_path = brain_path.rpartition("/")[0]
            if brain_parent_path == navtree_path:
                # This should be already provided by the portal_tabs_view
                continue
            if brain.exclude_from_nav and not context_path.startswith(brain_path):
                # skip excluded items if they're not in our context path
                continue
            url = brain.getURL()
            entry = {
                "path": brain_path,
                "@id": url,
                "title": safe_unicode(brain.Title),
                "description": safe_unicode(brain.Description),
                "review_state": json_compatible(brain.review_state),
                "use_view_action_in_listings": brain.portal_type in types_using_view,
            }

            if brain.get("nav_title", False):
                entry.update({"title": brain["nav_title"]})

            self.customize_entry(entry, brain)
            ret[brain_parent_path].append(entry)
        return ret

    def customize_entry(self, entry, brain):
        """a little helper to add custom entry keys/values."""
        pass

    def render_item(self, item, path):
        sub = self.build_tree(item["path"], first_run=False)

        item.update({"items": sub})

        if "title" in item and item["title"]:
            item["title"] = item["title"]
        if "path" in item:
            del item["path"]
        return item

    def build_tree(self, path, first_run=True):
        """Non-template based recursive tree building.
        3-4 times faster than template based.
        """
        out = []
        for item in self.navtree.get(path, []):
            out.append(self.render_item(item, path))

        return out


class CusyNavigationGet(Service):
    def reply(self):
        navigation = CusyNavigation(self.context, self.request)
        return navigation(expand=True)["navigation"]
