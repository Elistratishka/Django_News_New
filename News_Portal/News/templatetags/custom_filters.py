from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    bad_words = ['kaka', 'saka', 'nigga']
    text = set(value.split())
    for i in text:
        for j in bad_words:
            if i == j:
                return value.replace(i, '***')
    return value
