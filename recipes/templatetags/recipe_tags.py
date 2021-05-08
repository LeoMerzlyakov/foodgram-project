from django import template
from recipes.models import Follow, Purchase


register = template.Library()

@register.simple_tag(name='is_in_purchase')
def is_in_purchase(user, recipe):
    return Purchase.objects.filter(user=user, recipe=recipe).exists()


@register.simple_tag()
def purchase_count(user):
    return Purchase.objects.filter(user=user).count()

@register.simple_tag()
def is_subscubed(user, author):
    subs = Follow.objects.filter(user=user, author=author).exists()
    return subs
