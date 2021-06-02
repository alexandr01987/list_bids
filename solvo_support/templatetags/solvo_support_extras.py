from django import template

register = template.Library()


@register.filter(name='get_property')
def get_property(value, arg):
    return getattr(value, arg)
