from django.template.defaultfilters import register

@register.filter
def dictitem(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_management_form(value):
    return value.management_form

@register.filter
def type_bootstrap_class(value):
    if value == 'A':
        return 'bg-info'
    if value == 'M':
        return 'bg-light text-dark'
    else:
        return 'bg-dark'

@register.filter
def status_bootstrap_class(value):
    if value == 'S':
        return 'bg-light text-dark'
    if value == 'P':
        return 'bg-success'
    if value == 'E':
        return 'bg-warning text-dark'
    if value == 'F':
        return 'bg-danger'
    else:
        return 'bg-dark'

@register.filter
def priority_bootstrap_class(value):
    if value == 'L':
        return 'bg-info'
    if value == 'M':
        return 'bg-warning text-dark'
    if value == 'H':
        return 'bg-danger'
    else:
        return 'bg-dark'