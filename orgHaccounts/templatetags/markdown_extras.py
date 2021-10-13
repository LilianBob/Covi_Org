from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def new_markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.md_in_html'])