from django import template
from recipes.models import Purchase


register = template.Library()

@register.simple_tag(name='is_in_purchase')
def is_in_purchase(user, recipe):
    return Purchase.objects.filter(user=user, recipe=recipe).exists()


@register.simple_tag()
def purchase_count(user):
    return Purchase.objects.filter(user=user).count()
