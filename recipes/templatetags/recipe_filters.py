from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter()
@stringfilter
def check_tags(selected_tags, current_tag):
    # В списке 'selected_tags' может прийти не более 3х уникальных
    # элементов: B L D.
    # Элемент 'current_tug' - выбранный в checkbox элемент B/D/L
    selected_tags = list(selected_tags)
    if current_tag in selected_tags:
        selected_tags.remove(current_tag)
    else:
        selected_tags.append(current_tag)

    selected_tags = ''.join(selected_tags)
    return selected_tags
