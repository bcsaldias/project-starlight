import hashlib, urllib
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='get_range')
def get_range(value):
    return range(value)


@register.filter(name='paginate')
def paginate(value1, value2):
    per_page = 20
    value1 = int(value1)
    value2 = (int(value2)-1) * per_page
    return value1 + value2

@register.filter(name='badge')
def badge(level, size=120):
    src = "/static/img/badges/level-"+str(level)+".svg"
    return mark_safe("<img src='%s' width='%s' class='center-block'>" % (src, size))



@register.filter
def gravatar_url(email, size=40):
  default = "retro"
  return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower().encode('utf-8')).hexdigest(), urllib.parse.urlencode({'d':default, 's':str(size)}))


@register.filter
def gravatar(email, size=40):
    url = gravatar_url(email, size)
    return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))
