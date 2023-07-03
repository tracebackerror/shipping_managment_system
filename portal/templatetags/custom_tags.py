from django import template

from portal.utils import getPortFullName
register = template.Library()

@register.filter(name='get_port_name')
def getPortName(port_code):
    return getPortFullName(port_code)
