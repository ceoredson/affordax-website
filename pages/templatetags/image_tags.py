from django import template


register = template.Library()


@register.simple_tag
def image_source_exists(image):
    """Return whether a Wagtail image's original file still exists in storage."""
    if not image or not image.file:
        return False
    try:
        return image.file.storage.exists(image.file.name)
    except (OSError, ValueError):
        return False
