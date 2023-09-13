# user_filters.py
from django import template
from datetime import datetime, timedelta


register = template.Library()


@register.filter
def next_date(value):
    try:
        date_obj = datetime.fromisoformat(value).date()
        next_date_obj = date_obj + timedelta(days=1)
        return next_date_obj.isoformat()
    except ValueError:
        return value


@register.filter
def previous_date(value):
    try:
        date_obj = datetime.fromisoformat(value).date()
        previous_date_obj = date_obj - timedelta(days=1)
        return previous_date_obj.isoformat()
    except ValueError:
        return value


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})
