from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

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
    
@register.filter(is_save=True)
def status_bootstrap_icon_class(value):
    if value == 'S' or 'None' or None:
        element = '<i class="bi bi-dash-circle-fill text-secondary h4" title="Пропущено"></i>'
    if value == 'P':
        element = '<i class="bi bi-check-circle-fill text-success h4" title="Успешно"></i>'
    if value == 'E':
        element = '<i class="bi bi-exclamation-circle-fill text-warning h4" title="Ошибка"></i>'
    if value == 'F':
        element = '<i class="bi bi-x-circle-fill text-danger h4" title="Провал"></i>'

    return mark_safe(element)

@register.filter(is_save=True)
def type_bootstrap_icon_class(value):
    if value == 'A':
        element = '<i class="bi bi-rocket-takeoff-fill h4 text-primary" title="Автотест"></i>'
    if value == 'M':
        element = '<i class="bi bi-hand-index-thumb-fill h4 text-warning" title="Ручной"></i>'
    
    return mark_safe(element)

@register.filter
def status_bootstrap_background_class_for_teststep(value):
    if value == 'S':
        return 'bg-light text-dark'
    if value == 'E':
        return 'bg-warning text-dark'
    if value == 'F':
        return 'bg-danger'
    else:
        return
    
@register.filter
def duration(td):
    print(td)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return '{} hours {} min'.format(hours, minutes)
    