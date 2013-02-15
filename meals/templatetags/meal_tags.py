from django import template
from django.core.urlresolvers import reverse 

from ..utils import get_eaten_meal
from ..settings import LEVEL_CHOICES_QUICKACCESS

register = template.Library()

@register.simple_tag
def have_eaten_url(meal, post_query):
    POST = post_query.copy()
    del POST['csrfmiddlewaretoken']
    
    http_get_string = POST.urlencode()
    for key in POST.iterkeys():
        http_get_string += key + '=' + POST[key] + '&'
    
    # Removing the last ampersand
    http_get_string = http_get_string[:-1]
    
    return reverse('rdm_have_eaten', kwargs={'meal_id': meal.id}) + http_get_string

@register.simple_tag
def times_eaten(meal, user):
    eaten_meal = get_eaten_meal(user, meal)
    if eaten_meal.times is None:
        eaten_meal.times = 0
    eaten_meal.save()
    return eaten_meal.times

@register.filter
def german_price(value):
    """
    This filter converts a number into a german-formatted price.
    e.g. 8 -> 8,00
    """
    price = str(value)
    if price.find('.') != -1:
        eur, cents = price.split('.')
        if len(cents) == 1:
            cents += '0'
    else:
        eur, cents = (price, '00')
    
    return "%s,%s" % (eur, cents)

@register.inclusion_tag(
    'meals/chunks/level-value.html',
    takes_context=True
)
def nice_level_value(context, numeric_value):
    """
    This inclusion tag displays the numeric level value (e.g. Complexity)
    as a nice string including some markup to make it look nicer.
    """
    context.update({
        'level': LEVEL_CHOICES_QUICKACCESS[numeric_value][0],
        'color': LEVEL_CHOICES_QUICKACCESS[numeric_value][1]
    })
    return context