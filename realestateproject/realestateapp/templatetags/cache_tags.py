from django import template
from django.core.cache import cache

register = template.Library()

@register.simple_tag
def get_cache(key):
    return cache.get(key)
