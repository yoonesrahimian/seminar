from django import template

register = template.Library()

@register.filter
def bootstrap_alert_class(tags):
    mapping = {
        'success': 'success',
        'warning': 'warning',
        'info': 'info',
        'error': 'danger',
    }
    return mapping.get(tags, 'info')