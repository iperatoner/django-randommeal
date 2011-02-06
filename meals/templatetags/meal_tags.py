from django import template
from django.core.urlresolvers import reverse 

from ..utils import get_eaten_meal

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