from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter()
@stringfilter
def check_tags(selected_tags, current_tag):
    selected_tags = list(selected_tags)
    if current_tag in selected_tags:
        selected_tags = list(
            filter(lambda tag: tag != current_tag, selected_tags)
        )
    else:
        selected_tags.append(current_tag)

    selected_tags = ''.join(selected_tags)
    return selected_tags
