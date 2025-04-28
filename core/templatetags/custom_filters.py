from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(field, css_class):
    """
    Добавляет CSS класс к виджету поля формы.
    """
    if hasattr(field, 'field') and hasattr(field.field.widget, 'attrs'):
        field.field.widget.attrs['class'] = field.field.widget.attrs.get('class', '') + f' {css_class}'
    return field
