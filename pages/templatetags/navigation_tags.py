from django import template
from wagtail.models import Site

register = template.Library()


@register.inclusion_tag("includes/navigation.html", takes_context=True)
def primary_navigation(context):
    request = context["request"]
    site = Site.find_for_request(request)
    if site is None:
        return {"items": [], "current_page": context.get("page")}
    items = site.root_page.get_children().live().in_menu().specific()
    return {"items": items, "current_page": context.get("page")}
