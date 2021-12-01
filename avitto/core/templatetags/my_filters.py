from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


def currency(rub):
    rub = round(float(rub), 2)
    return "%s%s" % (intcomma(int(rub)), ("%0.2f" % rub)[-3:])


register.filter('currency', currency)
