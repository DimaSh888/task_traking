from django import template


register = template.Library()


@register.filter(name="endswith_any")
def endswith_any(value, extensions):
    if not value:
        return False

    value = str(value).lower()
    extensions = [ext.strip().lower() for ext in extensions.split(",")]

    return any(value.endswith(ext) for ext in extensions)
