from django.template.defaultfilters import register

@register.filter
def dictitem(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_management_form(value):
    return value.management_form