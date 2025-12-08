from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Returns dictionary[key] or None if not found"""
    return dictionary.get(key)